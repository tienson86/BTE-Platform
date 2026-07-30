"""Integration tests: Ten Gods Engine + Analysis Runtime."""

from __future__ import annotations

import pytest

from engines.analysis_engine.runtime import AnalysisContext, AnalysisRuntime, StageResult
from engines.analysis_engine.runtime.base_module import BaseAnalysisModule
from engines.analysis_engine.ten_gods_engine import (
    TenGodsEngine,
    TenGodsResult,
    create_default_knowledge_session,
)


class UpstreamStub(BaseAnalysisModule):
    """Deterministic upstream stub with fixed classification payload."""

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


def _build_partial_runtime() -> AnalysisRuntime:
    runtime = AnalysisRuntime(
        require_all_canonical_stages=False,
        knowledge_binder=_bind_knowledge,
    )
    runtime.register(
        UpstreamStub("strength", {"classification": "strong", "score": 0.8})
    )
    runtime.register(
        UpstreamStub(
            "temperature",
            {"classification": "cold"},
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
            {
                "useful_gods": ["zheng_guan"],
                "favorable": ["zheng_guan"],
                "unfavorable": ["shang_guan"],
            },
            dependencies=("strength", "temperature", "pattern"),
        )
    )
    runtime.register(TenGodsEngine())
    return runtime


def test_runtime_pipeline_publishes_ten_gods_result() -> None:
    runtime = _build_partial_runtime()
    context = AnalysisContext(
        request_id="tg-int-001",
        chart={
            "day_master": "Giáp",
            "stems": {
                "year": "Canh",
                "month": "Bính",
                "day": "Giáp",
                "hour": "Mậu",
            },
        },
    )
    result = runtime.run(context)

    assert result.ten_gods_result is not None
    assert result.ten_gods_result.stage_id == "ten_gods"
    typed = TenGodsResult.from_stage_result(result.ten_gods_result)
    assert typed.presence
    assert typed.confidence.score is not None
    assert typed.knowledge_module_id == "ten_gods_knowledge"
    assert context.ten_gods_result is result.ten_gods_result


def test_runtime_execute_ten_gods_after_upstream() -> None:
    runtime = _build_partial_runtime()
    context = AnalysisContext(
        request_id="tg-int-002",
        chart={
            "day_master": "Giáp",
            "stems": {
                "year": "Canh",
                "month": "Bính",
                "day": "Giáp",
                "hour": "Mậu",
            },
        },
    )
    for stage_id in ("strength", "temperature", "pattern", "useful_god"):
        runtime.execute(stage_id, context)

    stage = runtime.execute("ten_gods", context)
    typed = TenGodsResult.from_stage_result(stage)
    assert typed.summary["presence_count"] == len(typed.presence)


def test_deterministic_across_runtime_runs() -> None:
    runtime = _build_partial_runtime()

    def run_once(request_id: str) -> dict:
        context = AnalysisContext(
            request_id=request_id,
            chart={
                "day_master": "Giáp",
                "stems": {
                    "year": "Canh",
                    "month": "Bính",
                    "day": "Giáp",
                    "hour": "Mậu",
                },
            },
        )
        result = runtime.run(context)
        assert result.ten_gods_result is not None
        payload = dict(result.ten_gods_result.payload)
        # Diagnostics message is stable; request_id is not embedded in payload.
        return payload

    assert run_once("a") == run_once("b")


def test_ten_gods_reads_only_shared_context_upstream() -> None:
    runtime = _build_partial_runtime()
    context = AnalysisContext(
        request_id="tg-int-003",
        chart={
            "day_master": "Ất",
            "stems": {
                "year": "Giáp",
                "month": "Canh",
                "day": "Ất",
                "hour": "Nhâm",
            },
        },
    )
    result = runtime.run(context)
    assert result.strength_result is not None
    assert result.useful_god_result is not None
    typed = TenGodsResult.from_stage_result(result.ten_gods_result)  # type: ignore[arg-type]
    # Ất (Yin Wood) + Giáp (Yang Wood) => jie_cai
    assert any(item.god_id == "jie_cai" for item in typed.presence)
