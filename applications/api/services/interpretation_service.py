"""Interpretation service coordination layer."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from time import perf_counter

from applications.api.adapters.interpretation_adapter import InterpretationAdapter
from applications.api.contracts.analyze_request import AnalyzeRequest
from applications.api.contracts.report_response import (
    AnalysisPayload,
    BasicInformationInfo,
    ChartPayload,
    DiagnosticsPayload,
    FourPillarsInfo,
    HiddenStemsInfo,
    LayoutInfo,
    Metadata,
    PatternInfo,
    RelationshipInfo,
    RenderOptionsInfo,
    ReportPayload,
    ReportResponse,
    ScoreInfo,
    StrengthInfo,
    SummaryInfo,
    ThemeInfo,
    UsefulGodInfo,
)
from applications.api.contracts.version import API_VERSION, SCHEMA_VERSION


class InterpretationService(ABC):
    """Coordinates interpretation requests without business logic."""

    @abstractmethod
    def execute(self, request: AnalyzeRequest) -> ReportResponse:
        """Execute interpretation through the adapter boundary."""


class DefaultInterpretationService(InterpretationService):
    """Interpretation service that delegates to InterpretationAdapter."""

    def __init__(self, adapter: InterpretationAdapter | None = None) -> None:
        self._adapter = adapter or InterpretationAdapter()

    def execute(self, request: AnalyzeRequest) -> ReportResponse:
        """Delegate interpretation execution to the adapter."""
        started = perf_counter()
        timestamp = datetime.now(timezone.utc)
        result = self._adapter.execute(request)
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
            chart=ChartPayload(
                four_pillars=FourPillarsInfo(),
                hidden_stems=HiddenStemsInfo(),
                luck_cycles=[],
                basic_information=BasicInformationInfo(),
            ),
            analysis=AnalysisPayload(
                scores=ScoreInfo(),
                strength=StrengthInfo(),
                useful_god=UsefulGodInfo(),
                pattern=PatternInfo(),
                relationships=RelationshipInfo(),
                summary=SummaryInfo(),
            ),
            interpretation=result.interpretation,
            report=ReportPayload(
                title=request.report_template,
                blocks=[],
                theme=ThemeInfo(name=request.report_template),
                layout=LayoutInfo(name=request.report_template),
                render_options=RenderOptionsInfo(
                    format="json",
                    locale=request.language,
                ),
            ),
            diagnostics=DiagnosticsPayload(
                warnings=[],
                validation_errors=[],
                runtime_messages=[],
                debug_info=None,
            ),
        )
