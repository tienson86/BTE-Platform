"""Analysis service coordination layer."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from time import perf_counter

from applications.api.adapters.analysis_adapter import (
    AnalysisAdapter,
    extract_birth_kwargs,
    map_analysis_payload,
    map_chart_payload,
)
from applications.api.adapters.interpretation_adapter import (
    InterpretationAdapter,
    map_interpretation_payload,
)
from applications.api.adapters.report_adapter import ReportAdapter, map_report_payload
from applications.api.contracts.analyze_request import AnalyzeRequest
from applications.api.contracts.report_response import (
    DiagnosticsPayload,
    Metadata,
    ReportResponse,
)
from applications.api.contracts.version import API_VERSION, SCHEMA_VERSION
from applications.api.services.orchestrator import OrchestratorService


class AnalysisService(ABC):
    """Coordinates analysis requests without business logic."""

    @abstractmethod
    def execute(self, request: AnalyzeRequest) -> ReportResponse:
        """Execute analysis through the adapter boundary."""


class DefaultAnalysisService(AnalysisService):
    """Orchestrates Analysis → Interpretation → Report adapters."""

    def __init__(
        self,
        adapter: AnalysisAdapter | None = None,
        interpretation_adapter: InterpretationAdapter | None = None,
        report_adapter: ReportAdapter | None = None,
        orchestrator: OrchestratorService | None = None,
    ) -> None:
        shared = orchestrator or OrchestratorService()
        self._orchestrator = shared
        self._adapter = adapter or AnalysisAdapter(orchestrator=shared)
        self._interpretation_adapter = interpretation_adapter or InterpretationAdapter(
            orchestrator=shared
        )
        self._report_adapter = report_adapter or ReportAdapter(orchestrator=shared)

    def execute(self, request: AnalyzeRequest) -> ReportResponse:
        """
        Orchestrate the integration pipeline from one analyze() run.

        AnalyzeRequest
            → OrchestratorService.analyze
            → adapters map chart / interpretation / report / narrative_result
            → ReportResponse
        """
        started = perf_counter()
        timestamp = datetime.now(timezone.utc)
        engine_payload = self._orchestrator.analyze(**extract_birth_kwargs(request))
        raw_narrative = engine_payload.get("narrative_result")
        narrative_result = raw_narrative if isinstance(raw_narrative, dict) else None

        elapsed_ms = int((perf_counter() - started) * 1000)
        return ReportResponse(
            success=True,
            metadata=Metadata(
                request_id=request.request_id,
                timestamp=timestamp,
                api_version=request.api_version or API_VERSION,
                schema_version=SCHEMA_VERSION,
                engine_version=API_VERSION,
                knowledge_version=SCHEMA_VERSION,
                processing_time_ms=elapsed_ms,
            ),
            chart=map_chart_payload(engine_payload, request),
            analysis=map_analysis_payload(engine_payload),
            interpretation=map_interpretation_payload(engine_payload),
            report=map_report_payload(engine_payload, request),
            diagnostics=DiagnosticsPayload(
                warnings=[],
                validation_errors=[],
                runtime_messages=[],
                debug_info=None,
            ),
            narrative_result=narrative_result,
        )
