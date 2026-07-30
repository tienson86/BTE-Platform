"""Analysis execution service using Analysis Runtime."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.api.services.store import (
    AnalysisRecord,
    ResourceStore,
    new_id,
)
from engines.analysis_engine.runtime import AnalysisContext, AnalysisRuntime, StageResult
from engines.analysis_engine.runtime.base_module import BaseAnalysisModule
from engines.analysis_engine.runtime.models import ConfidenceEvaluation, RuleEvidence
from engines.analysis_engine.summary_engine import SummaryEngine


class UpstreamStub(BaseAnalysisModule):
    """Deterministic analytical stub for stages without dedicated API wiring."""

    def __init__(
        self,
        stage_id: str,
        payload: dict[str, Any],
        *,
        confidence: float = 0.8,
        dependencies: tuple[str, ...] = (),
    ) -> None:
        super().__init__(stage_id=stage_id, dependencies=dependencies)
        self._payload = payload
        self._confidence = confidence

    def evaluate(self, context: AnalysisContext) -> StageResult:
        return StageResult(
            stage_id=self.stage_id,
            module_version=self.version,
            payload=dict(self._payload),
            confidence=ConfidenceEvaluation(score=self._confidence, level="high"),
            evidence=[
                RuleEvidence(
                    rule_id=f"{self.stage_id}:api_stub",
                    category=self.stage_id,
                    priority=10,
                    reference="analysis_api",
                )
            ],
        )


def build_analysis_runtime() -> AnalysisRuntime:
    """Build runtime with stubs for 01–08 and SummaryEngine for 09."""
    runtime = AnalysisRuntime(require_all_canonical_stages=False)
    specs: list[tuple[str, dict[str, Any], float, tuple[str, ...]]] = [
        ("strength", {"classification": "strong", "score": 0.82}, 0.9, ()),
        ("temperature", {"classification": "balanced"}, 0.8, ("strength",)),
        (
            "pattern",
            {"pattern_id": "zheng_guan_ge", "name": "Zheng Guan Ge"},
            0.85,
            ("strength", "temperature"),
        ),
        (
            "useful_god",
            {
                "useful_gods": ["zheng_guan", "shi_shen"],
                "favorable": ["zheng_guan"],
                "unfavorable": ["shang_guan"],
            },
            0.7,
            ("strength", "temperature", "pattern"),
        ),
        (
            "ten_gods",
            {"presence": [{"god_id": "zheng_guan"}]},
            0.88,
            ("strength", "temperature", "pattern", "useful_god"),
        ),
        (
            "combination",
            {"clashes": []},
            0.72,
            ("strength", "temperature", "pattern", "useful_god", "ten_gods"),
        ),
        (
            "shensha",
            {"presence": [{"shensha_id": "tianyi_guiren"}], "auspicious": []},
            0.77,
            (
                "strength",
                "temperature",
                "pattern",
                "useful_god",
                "ten_gods",
                "combination",
            ),
        ),
        (
            "luck",
            {"summary": {"active_count": 4, "current_da_yun_index": 2}},
            0.75,
            (
                "strength",
                "temperature",
                "pattern",
                "useful_god",
                "ten_gods",
                "combination",
                "shensha",
            ),
        ),
    ]
    for stage_id, payload, confidence, deps in specs:
        runtime.register(
            UpstreamStub(
                stage_id,
                payload,
                confidence=confidence,
                dependencies=deps,
            )
        )
    runtime.register(SummaryEngine())
    return runtime


class AnalysisService:
    """Execute Analysis Runtime for a stored chart."""

    def __init__(
        self,
        store: ResourceStore,
        *,
        runtime: AnalysisRuntime | None = None,
    ) -> None:
        self._store = store
        self._runtime = runtime or build_analysis_runtime()

    def analyze(self, chart_id: str) -> AnalysisRecord:
        """Run analysis pipeline and persist AnalysisResult snapshot."""
        chart = self._store.get_chart(chart_id)
        analysis_id = new_id("anl")
        context = AnalysisContext(
            request_id=analysis_id,
            chart=dict(chart.chart),
            calendar=dict(chart.calendar),
            metadata={"chart_id": chart_id, **dict(chart.metadata)},
        )
        result = self._runtime.run(context)
        stage_payloads = {
            stage_id: dict(stage.payload)
            for stage_id, stage in result.stage_results.items()
        }
        payload = {
            "analysis_id": analysis_id,
            "chart_id": chart_id,
            "request_id": result.request_id,
            "runtime_version": result.runtime_version,
            "knowledge_version": result.knowledge_version,
            "stage_ids": list(result.stage_results.keys()),
            "summary": (
                None
                if result.summary_result is None
                else dict(result.summary_result.payload)
            ),
            "confidence": None
            if result.confidence is None
            else {
                "score": result.confidence.score,
                "level": result.confidence.level,
                "details": dict(result.confidence.details),
            },
        }
        return self._store.put_analysis(
            AnalysisRecord(
                analysis_id=analysis_id,
                chart_id=chart_id,
                request_id=result.request_id,
                payload=payload,
                stage_payloads=stage_payloads,
            )
        )

    def get(self, analysis_id: str) -> AnalysisRecord:
        """Return a stored analysis."""
        return self._store.get_analysis(analysis_id)
