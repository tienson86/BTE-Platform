"""Analysis service coordination layer."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from time import perf_counter

from applications.api.adapters.analysis_adapter import AnalysisAdapter
from applications.api.adapters.interpretation_adapter import InterpretationAdapter
from applications.api.adapters.report_adapter import ReportAdapter
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
        self._adapter = adapter or AnalysisAdapter(orchestrator=shared)
        self._interpretation_adapter = interpretation_adapter or InterpretationAdapter(
            orchestrator=shared
        )
        self._report_adapter = report_adapter or ReportAdapter(orchestrator=shared)

    def execute(self, request: AnalyzeRequest) -> ReportResponse:
        """
        Orchestrate the integration pipeline.

        AnalyzeRequest
            → AnalysisAdapter
            → InterpretationAdapter
            → ReportAdapter
            → ReportResponse
        """
        started = perf_counter()
        timestamp = datetime.now(timezone.utc)

        analysis_result = self._adapter.execute(request)
        interpretation_result = self._interpretation_adapter.execute(request)
        report_result = self._report_adapter.execute(request)

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
            chart=analysis_result.chart,
            analysis=analysis_result.analysis,
            interpretation=interpretation_result.interpretation,
            report=report_result.report,
            diagnostics=DiagnosticsPayload(
                warnings=[],
                validation_errors=[],
                runtime_messages=[],
                debug_info=None,
            ),
        )
