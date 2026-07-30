"""Integration tests: Combination Engine + Analysis Runtime."""

from __future__ import annotations

from engines.analysis_engine.combination_engine import (
    CombinationEngine,
    CombinationResult,
    create_default_knowledge_session,
)
from engines.analysis_engine.runtime import AnalysisContext, AnalysisRuntime, StageResult
from engines.analysis_engine.runtime.base_module import BaseAnalysisModule


class UpstreamStub(BaseAnalysisModule):
    """Deterministic upstream stub."""

    def __init__(
        self,
        stage_id: str,
        payload: dict,
        dependencies: tuple[str, ...] = (),
    ) -> None:
        super().__init__(stage_id=stage_id, dependencies=dependencies)
        self._payload = payload

    def evaluate(self, context: AnalysisContext) -> StageResult:
        return StageResult(
            stage_id=self.stage_id,
            module_version=self.version,
            payload=dict(self._payload),
        )


def _bind_knowledge(context: AnalysisContext) -> None:
    context.knowledge_session = create_default_knowledge_session()
    context.knowledge_version = "1.0.0"


def _build_runtime() -> AnalysisRuntime:
    runtime = AnalysisRuntime(
        require_all_canonical_stages=False,
        knowledge_binder=_bind_knowledge,
    )
    runtime.register(UpstreamStub("strength", {"classification": "strong"}))
    runtime.register(
        UpstreamStub(
            "temperature",
            {"classification": "balanced"},
            dependencies=("strength",),
        )
    )
    runtime.register(
        UpstreamStub(
            "pattern",
            {"pattern_id": "zheng_guan_ge"},
            dependencies=("strength", "temperature"),
        )
    )
    runtime.register(
        UpstreamStub(
            "useful_god",
            {"useful_gods": ["zheng_guan"], "favorable": ["zheng_guan"]},
            dependencies=("strength", "temperature", "pattern"),
        )
    )
    runtime.register(
        UpstreamStub(
            "ten_gods",
            {
                "presence": [
                    {
                        "god_id": "zheng_guan",
                        "label": "Zheng Guan",
                        "source_pillar": "year",
                        "source_stem": "Canh",
                        "polarity_class": "officer",
                        "count": 1,
                    }
                ]
            },
            dependencies=("strength", "temperature", "pattern", "useful_god"),
        )
    )
    runtime.register(CombinationEngine())
    return runtime


def _sample_context(request_id: str) -> AnalysisContext:
    return AnalysisContext(
        request_id=request_id,
        chart={
            "day_master": "Giáp",
            "stems": {
                "year": "Giáp",
                "month": "Kỷ",
                "day": "Giáp",
                "hour": "Bính",
            },
            "branches": {
                "year": "Tý",
                "month": "Sửu",
                "day": "Ngọ",
                "hour": "Tuất",
            },
        },
    )


def test_runtime_pipeline_publishes_combination_result() -> None:
    runtime = _build_runtime()
    result = runtime.run(_sample_context("comb-int-001"))

    assert result.combination_result is not None
    assert result.combination_result.stage_id == "combination"
    typed = CombinationResult.from_stage_result(result.combination_result)
    assert typed.clashes or typed.stem_combinations or typed.branch_combinations
    assert typed.confidence.score is not None
    assert typed.knowledge_module_id == "combination_knowledge"


def test_runtime_execute_combination_after_upstream() -> None:
    runtime = _build_runtime()
    context = _sample_context("comb-int-002")
    for stage_id in (
        "strength",
        "temperature",
        "pattern",
        "useful_god",
        "ten_gods",
    ):
        runtime.execute(stage_id, context)

    stage = runtime.execute("combination", context)
    typed = CombinationResult.from_stage_result(stage)
    assert "active_count" in typed.summary


def test_deterministic_across_runtime_runs() -> None:
    runtime = _build_runtime()

    def run_once(request_id: str) -> dict:
        result = runtime.run(_sample_context(request_id))
        assert result.combination_result is not None
        return dict(result.combination_result.payload)

    assert run_once("a") == run_once("b")


def test_consumes_ten_gods_result_from_shared_context() -> None:
    runtime = _build_runtime()
    context = _sample_context("comb-int-003")
    result = runtime.run(context)

    assert result.ten_gods_result is not None
    assert result.combination_result is not None
    typed = CombinationResult.from_stage_result(result.combination_result)
    # Upstream ten gods presence triggers qualifier evidence.
    assert any(
        item.category == "upstream_qualifier" and "ten_gods" in item.rule_id
        for item in typed.evidence
    )
