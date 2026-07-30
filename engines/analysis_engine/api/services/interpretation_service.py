"""Interpretation service bridging Analysis API store → Interpretation Engine."""

from __future__ import annotations

from types import MappingProxyType

from engines.analysis_engine.api.services.store import (
    InterpretationRecord,
    ResourceStore,
    new_id,
)
from engines.analysis_engine.interpretation_engine import (
    InterpretationContext,
    InterpretationEngine,
    InterpretationResult,
    create_default_knowledge_session,
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
    """Rebuild AnalysisResult from stored stage payloads."""
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


class InterpretationService:
    """Run Interpretation Engine for a stored analysis."""

    def __init__(
        self,
        store: ResourceStore,
        *,
        engine: InterpretationEngine | None = None,
    ) -> None:
        self._store = store
        self._engine = engine or InterpretationEngine()
        self._knowledge = create_default_knowledge_session()

    def interpret(self, analysis_id: str) -> InterpretationRecord:
        """Produce and store InterpretationResult."""
        analysis = self._store.get_analysis(analysis_id)
        chart = self._store.get_chart(analysis.chart_id)
        analysis_result = _rebuild_analysis_result(
            request_id=analysis.request_id,
            stage_payloads=analysis.stage_payloads,
        )
        result: InterpretationResult = self._engine.interpret(
            InterpretationContext(
                analysis_result=analysis_result,
                chart=dict(chart.chart),
                knowledge_session=self._knowledge,
                knowledge_version="1.0.0",
                metadata={"analysis_id": analysis_id, "chart_id": analysis.chart_id},
            )
        )
        interpretation_id = new_id("int")
        payload = result.to_dict()
        payload["interpretation_id"] = interpretation_id
        payload["analysis_id"] = analysis_id
        payload["chart_id"] = analysis.chart_id
        return self._store.put_interpretation(
            InterpretationRecord(
                interpretation_id=interpretation_id,
                analysis_id=analysis_id,
                chart_id=analysis.chart_id,
                request_id=result.request_id,
                payload=payload,
            )
        )

    def get(self, interpretation_id: str) -> InterpretationRecord:
        """Return a stored interpretation."""
        return self._store.get_interpretation(interpretation_id)
