"""Public Analysis API service facade."""

from __future__ import annotations

from uuid import uuid4

from engines.analysis_engine.api.analysis_request import AnalysisRequest
from engines.analysis_engine.api.analysis_response import (
    AnalysisResponse,
    AnalysisResponseStatus,
)
from engines.analysis_engine.api.analysis_session import AnalysisSession
from engines.analysis_engine.context.context_factory import ContextFactory
from engines.analysis_engine.engine import AnalysisEngine
from engines.analysis_engine.exceptions.runtime_error import AnalysisRuntimeError
from engines.analysis_engine.models.analysis_context import AnalysisContext
from engines.analysis_engine.models.analysis_result import AnalysisResult
from engines.analysis_engine.results.result_aggregator import ResultAggregator


class AnalysisService:
    """Public service facade for Analysis Engine API interactions.

    Wires request → context → engine skeleton → response.
    Does not implement BaZi analysis algorithms.
    Distinct from ``api.services.analysis_service.AnalysisService`` (legacy FastAPI).
    """

    def __init__(
        self,
        *,
        engine: AnalysisEngine | None = None,
        context_factory: ContextFactory | None = None,
        result_aggregator: ResultAggregator | None = None,
    ) -> None:
        """Initialize facade dependencies."""
        self._engine = engine or AnalysisEngine()
        self._context_factory = context_factory or ContextFactory()
        self._result_aggregator = result_aggregator or ResultAggregator()
        self._sessions: dict[str, AnalysisSession] = {}

    @property
    def engine(self) -> AnalysisEngine:
        """Return the bound Analysis Engine skeleton."""
        return self._engine

    def open_session(self, *, pipeline_id: str | None = None) -> AnalysisSession:
        """Open a new analysis API session."""
        session = AnalysisSession(pipeline_id=pipeline_id)
        self._sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> AnalysisSession:
        """Return an existing session by identifier."""
        session = self._sessions.get(session_id)
        if session is None:
            raise AnalysisRuntimeError(f"analysis_session_not_found:{session_id}")
        return session

    def close_session(self, session_id: str) -> None:
        """Close and retain a session record."""
        session = self.get_session(session_id)
        session.close()

    def analyze(
        self,
        request: AnalysisRequest,
        *,
        session: AnalysisSession | None = None,
    ) -> AnalysisResponse:
        """Execute the public analyze facade for a request."""
        if not request.validate():
            return AnalysisResponse(
                request_id=request.request_id,
                success=False,
                status=AnalysisResponseStatus.INVALID,
                session_id=None if session is None else session.session_id,
                pipeline_id=request.pipeline_id,
                errors=("analysis_request_invalid",),
            )

        active_session = session
        if active_session is None and request.session_id is not None:
            active_session = self.get_session(request.session_id)
        if active_session is None:
            active_session = self.open_session(pipeline_id=request.pipeline_id)

        active_session.bind_request(request)
        context = self._build_context(request)
        active_session.bind_context(context)
        active_session.mark_submitted()

        try:
            result = self._engine.analyze(context)
            final_result = None
            status = AnalysisResponseStatus.COMPLETED
            if request.finalize:
                final_result = self._result_aggregator.aggregate_to_final(result)
                status = AnalysisResponseStatus.FINALIZED
            response = AnalysisResponse(
                request_id=request.request_id,
                success=result.success,
                status=status if result.success else AnalysisResponseStatus.FAILED,
                session_id=active_session.session_id,
                pipeline_id=request.pipeline_id,
                context_id=context.id,
                analysis_result=result,
                final_result=final_result,
                messages=("analysis_facade_completed",),
                metadata={"engine_schema_version": self._engine.config.schema_version},
            )
        except Exception as exc:  # noqa: BLE001 - facade boundary
            response = AnalysisResponse(
                request_id=request.request_id,
                success=False,
                status=AnalysisResponseStatus.FAILED,
                session_id=active_session.session_id,
                pipeline_id=request.pipeline_id,
                context_id=context.id,
                errors=(f"analysis_facade_error:{type(exc).__name__}:{exc}",),
            )

        active_session.complete(response)
        return response

    def finalize(
        self,
        result: AnalysisResult,
        *,
        request_id: str | None = None,
        session_id: str | None = None,
    ) -> AnalysisResponse:
        """Finalize an analysis result through the public facade."""
        try:
            final_result = self._result_aggregator.aggregate_to_final(result)
            return AnalysisResponse(
                request_id=request_id or str(uuid4()),
                success=final_result.success,
                status=(
                    AnalysisResponseStatus.FINALIZED
                    if final_result.success
                    else AnalysisResponseStatus.FAILED
                ),
                session_id=session_id,
                pipeline_id=result.pipeline_id,
                analysis_result=result,
                final_result=final_result,
                messages=("analysis_facade_finalized",),
            )
        except Exception as exc:  # noqa: BLE001 - facade boundary
            return AnalysisResponse(
                request_id=request_id or str(uuid4()),
                success=False,
                status=AnalysisResponseStatus.FAILED,
                session_id=session_id,
                pipeline_id=result.pipeline_id,
                analysis_result=result,
                errors=(f"analysis_finalize_error:{type(exc).__name__}:{exc}",),
            )

    def validate_request(self, request: AnalysisRequest) -> bool:
        """Validate a public analysis request structurally."""
        return request.validate()

    def _build_context(self, request: AnalysisRequest) -> AnalysisContext:
        """Build an Analysis Context from a public request."""
        return self._context_factory.create(
            pipeline_id=request.pipeline_id,
            context_id=request.context_id or str(uuid4()),
            chart_id=request.chart_id,
            attributes=dict(request.attributes),
            version=request.version,
            metadata=dict(request.metadata),
            trace=(f"request:{request.request_id}",),
        )
