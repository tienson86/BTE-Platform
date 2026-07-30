"""Integration tests for Analysis Runtime pipeline orchestration."""

from __future__ import annotations

import pytest

from engines.analysis_engine.runtime import (
    AnalysisContext,
    AnalysisRuntime,
    CacheManager,
    StageExecutionError,
    StageResult,
)
from engines.analysis_engine.runtime.constants import CANONICAL_STAGES
from tests.analysis_runtime.conftest import (
    FailingModule,
    StubModule,
    make_stub,
    register_all_stubs,
)


def test_sequential_shared_context_propagation(
    runtime: AnalysisRuntime,
    context: AnalysisContext,
) -> None:
    register_all_stubs(runtime)
    result = runtime.run(context)

    # Each stage sees prior payloads through shared context.
    luck_payload = result.luck_result.payload if result.luck_result else {}
    assert luck_payload["upstream"]["strength"]["stage"] == "strength"
    assert result.summary_result is not None
    assert "luck" in result.summary_result.payload["upstream"]


def test_deterministic_repeated_runs(
    runtime: AnalysisRuntime,
    context: AnalysisContext,
) -> None:
    register_all_stubs(runtime)

    first = runtime.run(
        AnalysisContext(
            request_id="det-1",
            chart=dict(context.chart),
            calendar=dict(context.calendar),
            metadata=dict(context.metadata),
            knowledge_version=context.knowledge_version,
        )
    )
    second = runtime.run(
        AnalysisContext(
            request_id="det-2",
            chart=dict(context.chart),
            calendar=dict(context.calendar),
            metadata=dict(context.metadata),
            knowledge_version=context.knowledge_version,
        )
    )

    for stage_id in CANONICAL_STAGES:
        left = first.get_stage_result(stage_id)
        right = second.get_stage_result(stage_id)
        assert left is not None and right is not None
        assert left.payload["stage"] == right.payload["stage"]
        assert left.payload["day_master"] == right.payload["day_master"]


def test_dependency_injection_of_cache_and_binder(
    context: AnalysisContext,
) -> None:
    calls: list[str] = []

    def binder(ctx: AnalysisContext) -> None:
        calls.append(ctx.request_id)
        ctx.knowledge_session = {"bound": True}
        ctx.knowledge_version = "bound-v1"

    runtime = AnalysisRuntime(
        cache_manager=CacheManager(),
        knowledge_binder=binder,
        require_all_canonical_stages=True,
    )
    register_all_stubs(runtime)
    result = runtime.run(context)

    assert calls == [context.request_id]
    assert result.knowledge_version == "bound-v1"
    assert context.knowledge_session == {"bound": True}


def test_execution_trace_and_metrics(
    runtime: AnalysisRuntime,
    context: AnalysisContext,
) -> None:
    register_all_stubs(runtime)
    result = runtime.run(context)

    span_names = [span.name for span in result.execution_trace.spans]
    assert span_names == [f"stage:{stage}" for stage in CANONICAL_STAGES]
    assert all(span.status == "success" for span in result.execution_trace.spans)
    assert len(result.performance_metrics.stage_metrics) == len(CANONICAL_STAGES)


def test_fail_closed_stops_pipeline(
    runtime: AnalysisRuntime,
    context: AnalysisContext,
) -> None:
    for stage_id in CANONICAL_STAGES:
        if stage_id == "pattern":
            runtime.register(FailingModule(stage_id=stage_id, dependencies=("strength", "temperature")))
        else:
            runtime.register(make_stub(stage_id))

    with pytest.raises(StageExecutionError) as exc_info:
        runtime.run(context)

    assert exc_info.value.stage_id == "pattern"
    # Prior stages published; failed stage and later stages are absent.
    assert context.has_stage_result("strength")
    assert context.has_stage_result("temperature")
    assert not context.has_stage_result("pattern")
    assert not context.has_stage_result("summary")


def test_validate_then_run_workflow(
    runtime: AnalysisRuntime,
    context: AnalysisContext,
) -> None:
    register_all_stubs(runtime)
    report = runtime.validate(context)
    assert report.is_valid is True
    result = runtime.run(context)
    assert isinstance(result.stage_results["summary"], StageResult)


def test_partial_pipeline_when_not_requiring_all(
    partial_runtime: AnalysisRuntime,
    context: AnalysisContext,
) -> None:
    partial_runtime.register(make_stub("strength"))
    partial_runtime.register(make_stub("temperature"))
    result = partial_runtime.run(context)
    assert set(result.stage_results.keys()) == {"strength", "temperature"}
    assert result.temperature_result is not None


def test_module_reads_only_shared_context(
    runtime: AnalysisRuntime,
    context: AnalysisContext,
) -> None:
    class ObservingSummary(StubModule):
        def evaluate(self, context: AnalysisContext) -> StageResult:
            assert context.strength_result is not None
            assert context.luck_result is not None
            return StageResult(
                stage_id=self.stage_id,
                payload={"seen": list(context.published_stage_ids())},
            )

    for stage_id in CANONICAL_STAGES:
        if stage_id == "summary":
            runtime.register(ObservingSummary(stage_id="summary"))
        else:
            runtime.register(make_stub(stage_id))

    result = runtime.run(context)
    assert result.summary_result is not None
    assert result.summary_result.payload["seen"][-1] == "luck"
