"""Public Analysis Engine API facade entrypoint."""

from __future__ import annotations

from engines.analysis_engine.api.analysis_request import AnalysisRequest
from engines.analysis_engine.api.analysis_response import AnalysisResponse
from engines.analysis_engine.api.analysis_service import AnalysisService
from engines.analysis_engine.api.analysis_session import AnalysisSession
from engines.analysis_engine.config import AnalysisEngineConfig
from engines.analysis_engine.engine import AnalysisEngine
from engines.analysis_engine.exceptions.runtime_error import AnalysisRuntimeError
from engines.analysis_engine.interfaces.analysis_engine import AnalysisEngineInterface
from engines.analysis_engine.models.analysis_context import AnalysisContext
from engines.analysis_engine.models.analysis_result import AnalysisResult
from engines.analysis_engine.models.final_result import FinalResult


class AnalysisEngineAPI(AnalysisEngineInterface):
    """Public API facade for the Analysis Engine.

    Exposes analyze/finalize/validate boundaries without BaZi business logic.
    Coexists with the legacy FastAPI package under the same ``api/`` tree.
    """

    def __init__(
        self,
        *,
        config: AnalysisEngineConfig | None = None,
        engine: AnalysisEngine | None = None,
        service: AnalysisService | None = None,
    ) -> None:
        """Initialize the public API facade."""
        self._engine = engine or AnalysisEngine(config=config)
        self._service = service or AnalysisService(engine=self._engine)

    @property
    def service(self) -> AnalysisService:
        """Return the bound analysis service facade."""
        return self._service

    @property
    def engine(self) -> AnalysisEngine:
        """Return the bound Analysis Engine skeleton."""
        return self._engine

    def analyze(self, context: AnalysisContext) -> AnalysisResult:
        """Run analysis for a provided context via the engine skeleton."""
        return self._engine.analyze(context)

    def analyze_request(self, request: AnalysisRequest) -> AnalysisResponse:
        """Run analysis for a public API request and return an API response."""
        return self._service.analyze(request)

    def finalize(self, result: AnalysisResult) -> FinalResult:
        """Finalize an analysis result into a final aggregated result."""
        response = self._service.finalize(result)
        if response.final_result is None:
            raise AnalysisRuntimeError("analysis_finalize_missing_final_result")
        return response.final_result

    def validate_context(self, context: AnalysisContext) -> bool:
        """Validate that an analysis context is structurally acceptable."""
        return context.validate()

    def validate_request(self, request: AnalysisRequest) -> bool:
        """Validate a public analysis request."""
        return self._service.validate_request(request)

    def open_session(self, *, pipeline_id: str | None = None) -> AnalysisSession:
        """Open a public analysis session."""
        return self._service.open_session(pipeline_id=pipeline_id)

    def close_session(self, session_id: str) -> None:
        """Close a public analysis session."""
        self._service.close_session(session_id)
