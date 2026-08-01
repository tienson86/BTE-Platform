"""Tests for Pack 03 runtime execution pipeline."""

from __future__ import annotations

from engines.interpretation_engine.models.interpretation_result import InterpretationResult
from engines.interpretation_engine.models.section_result import SectionResult
from engines.interpretation_engine.orchestration.async_executor import (
    AsyncExecutionPlan,
    ExecutionMode,
    FutureAsyncExecutor,
)
from engines.interpretation_engine.orchestration.error_isolation import ErrorIsolator
from engines.interpretation_engine.orchestration.execution_pipeline import ExecutionPipeline
from engines.interpretation_engine.orchestration.section_collector import SectionCollector
from engines.interpretation_engine.runtime.contracts import HealthStatus
from engines.interpretation_engine.tests.runtime.conftest import (
    make_final_result,
    make_pack_context,
)
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.strength_interpreter import (
    StrengthInterpreter,
)
from engines.interpretation_engine.interpreter_runtime.registries.interpreter_registry import (
    InterpreterRegistration,
    InterpreterRegistry,
)
from engines.interpretation_engine.interpreter_runtime.dispatcher import (
    InterpreterDispatcher,
)


def test_execution_pipeline_happy_path() -> None:
    """Pipeline runs Context→Registry→Dispatcher→Interpreters→Sections→Explanation→Result."""
    pipeline = ExecutionPipeline(execution_mode=ExecutionMode.DEPENDENCY)
    pipeline.initialize()
    assert pipeline.validate() is True
    assert pipeline.health() is HealthStatus.READY

    result = pipeline.execute(make_pack_context(result_id="fr_exec_pipe"))
    assert result.success is True
    assert "execution_pipeline_ok" in result.messages
    assert result.payload["execution_mode"] == "dependency"
    assert len(result.payload["execution_order"]) == 12
    assert len(result.payload["sections"]) == 12
    assert result.payload["failed_interpreter_ids"] == []

    interpretation = result.payload["interpretation_result"]
    assert isinstance(interpretation, InterpretationResult)
    assert interpretation.validate() is True
    assert len(interpretation.sections) == 12
    assert interpretation.trace.stage_ids[0] == "registry"
    assert "section_collection" in interpretation.trace.stage_ids
    assert interpretation.trace.stage_ids[-1] == "explanation_runtime"

    # Dependency order: strength before pattern before summary.
    order = result.payload["execution_order"]
    assert order.index("strength_interpreter") < order.index("pattern_interpreter")
    assert order.index("scoring_interpreter") < order.index("summary_interpreter")

    pipeline.shutdown()
    assert pipeline.health() is HealthStatus.DISABLED


def test_execution_pipeline_ordered_and_future_async_modes() -> None:
    """Ordered and future_async modes resolve and execute."""
    ordered = ExecutionPipeline(execution_mode=ExecutionMode.ORDERED)
    ordered.initialize()
    result = ordered.execute(make_pack_context(result_id="fr_ordered"))
    assert result.success is True
    assert result.payload["execution_mode"] == "ordered"
    assert result.payload["execution_order"][0] == "strength_interpreter"

    async_mode = ExecutionPipeline(execution_mode=ExecutionMode.FUTURE_ASYNC)
    async_mode.initialize()
    result_async = async_mode.execute(make_pack_context(result_id="fr_async"))
    assert result_async.success is True
    assert result_async.payload["execution_mode"] == "future_async"
    assert len(result_async.payload["sections"]) == 12


def test_execution_pipeline_rejects_invalid_context() -> None:
    """Pipeline rejects non-pack / invalid contexts."""
    pipeline = ExecutionPipeline()
    pipeline.initialize()
    assert pipeline.execute(object()).success is False

    final = make_final_result(result_id="fr_bad_pipe")
    invalid = PackInterpretationContext(
        id="",
        version="1.0.0",
        pipeline_id="p",
        source_final_result_id=final.id,
        final_result=final,
        created_at="2026-01-01T00:00:00Z",
    )
    assert pipeline.execute(invalid).success is False


def test_error_isolation_keeps_pipeline_running() -> None:
    """One interpreter exception is isolated; other sections still collected."""

    class _Boom(StrengthInterpreter):
        interpreter_id = "strength_interpreter"
        section_type = "strength"

        def execute(self, context):  # type: ignore[override]
            raise RuntimeError("boom")

    dispatcher = InterpreterDispatcher()
    registry = InterpreterRegistry(dispatcher=dispatcher)
    boom = _Boom()
    boom.initialize()
    ok = StrengthInterpreter()
    ok.interpreter_id = "season_interpreter"
    ok.runtime_id = "season_interpreter"
    ok.section_type = "season"
    ok.initialize()

    registry.register_interpreter(
        InterpreterRegistration(
            interpreter_id="strength_interpreter",
            runtime=boom,
            priority=10,
            dependencies=(),
            section_type="strength",
            version="0.0.0-skeleton",
        )
    )
    registry.register_interpreter(
        InterpreterRegistration(
            interpreter_id="season_interpreter",
            runtime=ok,
            priority=20,
            dependencies=(),
            section_type="season",
            version="0.0.0-skeleton",
        )
    )
    # Mark as auto-registered so validate expects full set — disable auto for this test.
    registry._auto_registered = False  # noqa: SLF001

    pipeline = ExecutionPipeline(
        interpreter_registry=registry,
        dispatcher=dispatcher,
        auto_register=False,
        execution_mode=ExecutionMode.ORDERED,
    )
    pipeline.initialize()
    result = pipeline.execute(make_pack_context(result_id="fr_isolate"))
    assert result.success is True  # explanation ok; interpreter failures isolated
    assert "strength_interpreter" in result.payload["failed_interpreter_ids"]
    assert len(result.payload["sections"]) == 1
    assert result.payload["sections"][0].section_type == "season"


def test_section_collector_and_async_executor_helpers() -> None:
    """SectionCollector and FutureAsyncExecutor unit behavior."""
    collector = SectionCollector()
    section = SectionResult(
        id="section_x",
        section_type="strength",
        interpreter_id="strength_interpreter",
        paragraphs=(),
    )
    collected = collector.collect_from_dispatch(
        (
            ("strength_interpreter", {"success": True, "section": section}),
            ("season_interpreter", {"success": False, "messages": ("nope",)}),
            ("pattern_interpreter", None),
        )
    )
    assert collected.section_ids() == ("section_x",)
    assert collected.failed_interpreter_ids == (
        "season_interpreter",
        "pattern_interpreter",
    )
    assert collected.validate() is True

    isolator = ErrorIsolator()
    ok = isolator.run("a", lambda: 1)
    assert ok.success is True and ok.value == 1
    bad = isolator.run("b", lambda: (_ for _ in ()).throw(ValueError("x")))
    assert bad.success is False
    assert bad.error_type == "ValueError"

    executor = FutureAsyncExecutor(isolator=isolator)
    plan = AsyncExecutionPlan(
        mode=ExecutionMode.FUTURE_ASYNC,
        entry_ids=("a", "b"),
        allow_parallel=True,
    )
    assert plan.validate() is True
    results = executor.execute(plan, {"a": lambda: "A", "b": lambda: "B"})
    assert [item.value for item in results] == ["A", "B"]
