"""Report generation service bridging store → Report Generator."""

from __future__ import annotations

from types import MappingProxyType

from engines.analysis_engine.api.schemas import ReportRequest
from engines.analysis_engine.api.services.store import (
    ReportRecord,
    ResourceStore,
    new_id,
)
from engines.analysis_engine.interpretation_engine.models import InterpretationResult
from engines.analysis_engine.report_generator import (
    FormatProfile,
    ReportAssemblyContext,
    ReportGenerator,
)
from engines.analysis_engine.runtime.models import (
    AnalysisResult,
    ConfidenceEvaluation,
    ExecutionMetadata,
    ExecutionTrace,
    PerformanceMetrics,
    StageResult,
)


def _rebuild_analysis_result(
    *,
    request_id: str,
    stage_payloads: dict[str, dict],
) -> AnalysisResult:
    stage_results = {
        stage_id: StageResult(
            stage_id=stage_id,
            status="success",
            payload=dict(payload),
        )
        for stage_id, payload in stage_payloads.items()
    }
    return AnalysisResult(
        request_id=request_id,
        stage_results=MappingProxyType(stage_results),
        execution_metadata=ExecutionMetadata(
            request_id=request_id,
            status="success",
        ),
        performance_metrics=PerformanceMetrics(),
        execution_trace=ExecutionTrace(request_id=request_id),
        confidence=ConfidenceEvaluation(score=0.8, level="high"),
        strength_result=stage_results.get("strength"),
        temperature_result=stage_results.get("temperature"),
        pattern_result=stage_results.get("pattern"),
        useful_god_result=stage_results.get("useful_god"),
        ten_gods_result=stage_results.get("ten_gods"),
        combination_result=stage_results.get("combination"),
        shensha_result=stage_results.get("shensha"),
        luck_result=stage_results.get("luck"),
        summary_result=stage_results.get("summary"),
    )


class ReportService:
    """Assemble multi-format reports from stored interpretation."""

    def __init__(
        self,
        store: ResourceStore,
        *,
        generator: ReportGenerator | None = None,
    ) -> None:
        self._store = store
        self._generator = generator or ReportGenerator()

    def generate(self, body: ReportRequest) -> ReportRecord:
        """Produce and store ReportGeneratorResult."""
        interpretation = self._store.get_interpretation(body.interpretation_id)
        analysis = self._store.get_analysis(interpretation.analysis_id)
        interpretation_result = InterpretationResult.from_dict(interpretation.payload)
        analysis_result = None
        if body.include_structured_data:
            analysis_result = _rebuild_analysis_result(
                request_id=analysis.request_id,
                stage_payloads=analysis.stage_payloads,
            )
        profile = FormatProfile(
            formats=tuple(body.formats),
            require_analysis_result=body.include_structured_data,
            include_structured_data=body.include_structured_data,
            mandatory_sections=("overview",),
            title=body.title,
        )
        result = self._generator.assemble(
            ReportAssemblyContext(
                interpretation_result=interpretation_result,
                analysis_result=analysis_result,
                format_profile=profile,
                request_id=interpretation.request_id,
            )
        )
        report_id = new_id("rpt")
        payload = result.to_dict()
        payload["report_id"] = report_id
        payload["interpretation_id"] = interpretation.interpretation_id
        payload["analysis_id"] = interpretation.analysis_id
        payload["chart_id"] = interpretation.chart_id
        return self._store.put_report(
            ReportRecord(
                report_id=report_id,
                interpretation_id=interpretation.interpretation_id,
                analysis_id=interpretation.analysis_id,
                chart_id=interpretation.chart_id,
                request_id=interpretation.request_id,
                payload=payload,
            )
        )

    def get(self, report_id: str) -> ReportRecord:
        """Return a stored report."""
        return self._store.get_report(report_id)
