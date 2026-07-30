"""Integration tests: ShenSha Engine + Analysis Runtime."""

from __future__ import annotations

from engines.analysis_engine.runtime import AnalysisContext, AnalysisRuntime, StageResult
from engines.analysis_engine.runtime.base_module import BaseAnalysisModule
from engines.analysis_engine.shensha_engine import (
    ShenShaEngine,
    ShenShaResult,
    create_default_knowledge_session,
)


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
            {"useful_gods": ["zheng_guan"]},
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
            {
                "clashes": [
                    {
                        "relation_type": "clash",
                        "relation_id": "clash_zi_wu",
                        "members": ["Tý", "Ngọ"],
                        "pillars": ["year", "day"],
                        "status": "active",
                    }
                ]
            },
            dependencies=(
                "strength",
                "temperature",
                "pattern",
                "useful_god",
                "ten_gods",
            ),
        )
    )
    runtime.register(ShenShaEngine())
    return runtime


def _sample_context(request_id: str) -> AnalysisContext:
    return AnalysisContext(
        request_id=request_id,
        chart={
            "day_master": "Giáp",
            "stems": {
                "year": "Canh",
                "month": "Bính",
                "day": "Giáp",
                "hour": "Mậu",
            },
            "branches": {
                "year": "Tý",
                "month": "Sửu",
                "day": "Dậu",
                "hour": "Mão",
            },
        },
    )


def test_runtime_pipeline_publishes_shensha_result() -> None:
    runtime = _build_runtime()
    result = runtime.run(_sample_context("ss-int-001"))

    assert result.shensha_result is not None
    assert result.shensha_result.stage_id == "shensha"
    typed = ShenShaResult.from_stage_result(result.shensha_result)
    assert typed.presence
    assert typed.confidence.score is not None
    assert typed.knowledge_module_id == "shensha_knowledge"


def test_runtime_execute_shensha_after_upstream() -> None:
    runtime = _build_runtime()
    context = _sample_context("ss-int-002")
    for stage_id in (
        "strength",
        "temperature",
        "pattern",
        "useful_god",
        "ten_gods",
        "combination",
    ):
        runtime.execute(stage_id, context)

    stage = runtime.execute("shensha", context)
    typed = ShenShaResult.from_stage_result(stage)
    assert "presence_count" in typed.summary


def test_deterministic_across_runtime_runs() -> None:
    runtime = _build_runtime()

    def run_once(request_id: str) -> dict:
        result = runtime.run(_sample_context(request_id))
        assert result.shensha_result is not None
        return dict(result.shensha_result.payload)

    assert run_once("a") == run_once("b")


def test_consumes_combination_and_knowledge_sdk() -> None:
    runtime = _build_runtime()
    result = runtime.run(_sample_context("ss-int-003"))
    typed = ShenShaResult.from_stage_result(result.shensha_result)  # type: ignore[arg-type]
    assert any(item.category == "upstream_qualifier" for item in typed.evidence)
    assert any(item.category == "presence" for item in typed.evidence)
    assert any(item.shensha_id == "tianyi_guiren" for item in typed.auspicious)
