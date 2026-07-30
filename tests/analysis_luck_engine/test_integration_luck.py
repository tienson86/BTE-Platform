"""Integration tests: Luck Engine + Analysis Runtime."""

from __future__ import annotations

from engines.analysis_engine.luck_engine import (
    LuckEngine,
    LuckResult,
    create_default_knowledge_session,
)
from engines.analysis_engine.runtime import AnalysisContext, AnalysisRuntime, StageResult
from engines.analysis_engine.runtime.base_module import BaseAnalysisModule
from tests.analysis_luck_engine.conftest import sample_luck_block


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
            {"useful_gods": ["Kỷ", "Tỵ", "Thổ"], "favorable": ["Kỷ", "Tỵ", "Thổ"]},
            dependencies=("strength", "temperature", "pattern"),
        )
    )
    runtime.register(
        UpstreamStub(
            "ten_gods",
            {"presence": [{"god_id": "zheng_guan"}]},
            dependencies=("strength", "temperature", "pattern", "useful_god"),
        )
    )
    runtime.register(
        UpstreamStub(
            "combination",
            {"clashes": [{"relation_id": "clash_zi_wu"}]},
            dependencies=(
                "strength",
                "temperature",
                "pattern",
                "useful_god",
                "ten_gods",
            ),
        )
    )
    runtime.register(
        UpstreamStub(
            "shensha",
            {
                "presence": [{"shensha_id": "yangren"}],
                "inauspicious": [{"shensha_id": "yangren"}],
            },
            dependencies=(
                "strength",
                "temperature",
                "pattern",
                "useful_god",
                "ten_gods",
                "combination",
            ),
        )
    )
    runtime.register(LuckEngine())
    return runtime


def _sample_context(request_id: str) -> AnalysisContext:
    return AnalysisContext(
        request_id=request_id,
        chart={
            "day_master": "Giáp",
            "stems": {"day": "Giáp"},
            "luck": sample_luck_block(),
        },
    )


def test_runtime_pipeline_publishes_luck_result() -> None:
    runtime = _build_runtime()
    result = runtime.run(_sample_context("luck-int-001"))

    assert result.luck_result is not None
    assert result.luck_result.stage_id == "luck"
    typed = LuckResult.from_stage_result(result.luck_result)
    assert typed.da_yun
    assert typed.liu_nian
    assert typed.liu_yue
    assert typed.liu_ri
    assert typed.liu_shi
    assert typed.confidence.score is not None
    assert typed.knowledge_module_id == "luck_knowledge"


def test_runtime_execute_luck_after_upstream() -> None:
    runtime = _build_runtime()
    context = _sample_context("luck-int-002")
    for stage_id in (
        "strength",
        "temperature",
        "pattern",
        "useful_god",
        "ten_gods",
        "combination",
        "shensha",
    ):
        runtime.execute(stage_id, context)

    stage = runtime.execute("luck", context)
    typed = LuckResult.from_stage_result(stage)
    assert "active_count" in typed.summary
    assert typed.summary["current_da_yun_index"] == 3


def test_deterministic_across_runtime_runs() -> None:
    runtime = _build_runtime()

    def run_once(request_id: str) -> dict:
        result = runtime.run(_sample_context(request_id))
        assert result.luck_result is not None
        return dict(result.luck_result.payload)

    assert run_once("a") == run_once("b")


def test_hierarchy_and_upstream_interaction_evidence() -> None:
    runtime = _build_runtime()
    result = runtime.run(_sample_context("luck-int-003"))
    typed = LuckResult.from_stage_result(result.luck_result)  # type: ignore[arg-type]
    assert any(item.dimension == "strength" for item in typed.interactions)
    assert any(item.dimension == "useful_god" for item in typed.interactions)
    assert any(item.category == "da_yun" for item in typed.evidence)
    assert any(item.category == "liu_shi" for item in typed.evidence)
