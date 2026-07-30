"""Integration tests: Summary Engine + Analysis Runtime."""

from __future__ import annotations

from engines.analysis_engine.runtime import AnalysisContext, AnalysisRuntime, StageResult
from engines.analysis_engine.runtime.base_module import BaseAnalysisModule
from engines.analysis_engine.runtime.models import ConfidenceEvaluation, RuleEvidence
from engines.analysis_engine.summary_engine import SummaryEngine, SummaryResult
from engines.analysis_engine.summary_engine.models import UPSTREAM_STAGES


class UpstreamStub(BaseAnalysisModule):
    """Deterministic upstream stub."""

    def __init__(
        self,
        stage_id: str,
        payload: dict,
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
            confidence=ConfidenceEvaluation(
                score=self._confidence,
                level="high",
            ),
            evidence=[
                RuleEvidence(
                    rule_id=f"{self.stage_id}:stub",
                    category=self.stage_id,
                    priority=10,
                    reference="stub",
                )
            ],
        )


def _build_runtime() -> AnalysisRuntime:
    runtime = AnalysisRuntime(require_all_canonical_stages=False)
    specs: list[tuple[str, dict, float, tuple[str, ...]]] = [
        ("strength", {"classification": "strong"}, 0.9, ()),
        ("temperature", {"classification": "balanced"}, 0.8, ("strength",)),
        ("pattern", {"pattern_id": "zheng_guan_ge"}, 0.85, ("strength", "temperature")),
        (
            "useful_god",
            {"useful_gods": ["zheng_guan"]},
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


def test_runtime_pipeline_publishes_summary_result() -> None:
    runtime = _build_runtime()
    context = AnalysisContext(
        request_id="sum-int-001",
        chart={"day_master": "Giáp"},
    )
    result = runtime.run(context)

    assert result.summary_result is not None
    assert result.summary_result.stage_id == "summary"
    typed = SummaryResult.from_stage_result(result.summary_result)
    assert typed.consistency.status in {"pass", "warn"}
    assert typed.consolidated_confidence.score > 0
    assert set(typed.summary["stage_ids"]) == set(UPSTREAM_STAGES)


def test_runtime_execute_summary_after_upstream() -> None:
    runtime = _build_runtime()
    context = AnalysisContext(
        request_id="sum-int-002",
        chart={"day_master": "Giáp"},
    )
    for stage_id in UPSTREAM_STAGES:
        runtime.execute(stage_id, context)
    stage = runtime.execute("summary", context)
    typed = SummaryResult.from_stage_result(stage)
    assert typed.evidence_index
    assert typed.luck_summary.payload_digest["summary"]["size"] >= 1


def test_deterministic_across_runtime_runs() -> None:
    runtime = _build_runtime()

    def run_once(request_id: str) -> dict:
        result = runtime.run(
            AnalysisContext(
                request_id=request_id,
                chart={"day_master": "Giáp"},
            )
        )
        assert result.summary_result is not None
        return dict(result.summary_result.payload)

    assert run_once("a") == run_once("b")


def test_summary_indexes_all_upstream_evidence() -> None:
    runtime = _build_runtime()
    result = runtime.run(
        AnalysisContext(request_id="sum-int-003", chart={"day_master": "Giáp"})
    )
    typed = SummaryResult.from_stage_result(result.summary_result)  # type: ignore[arg-type]
    indexed_stages = {entry.stage_id for entry in typed.evidence_index}
    assert indexed_stages == set(UPSTREAM_STAGES)
