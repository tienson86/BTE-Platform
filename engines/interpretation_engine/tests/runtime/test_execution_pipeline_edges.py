"""Edge coverage for execution pipeline helpers."""

from __future__ import annotations

from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.interpreter_runtime.dispatcher import (
    InterpreterDispatcher,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.strength_interpreter import (
    StrengthInterpreter,
)
from engines.interpretation_engine.interpreter_runtime.registries.interpreter_registry import (
    InterpreterRegistration,
    InterpreterRegistry,
)
from engines.interpretation_engine.models.section_result import SectionResult
from engines.interpretation_engine.orchestration.async_executor import (
    AsyncExecutionPlan,
    ExecutionMode,
    FutureAsyncExecutor,
)
from engines.interpretation_engine.orchestration.error_isolation import (
    ErrorIsolator,
    IsolatedExecutionResult,
)
from engines.interpretation_engine.orchestration.execution_pipeline import ExecutionPipeline
from engines.interpretation_engine.orchestration.section_collector import SectionCollector
from engines.interpretation_engine.tests.runtime.conftest import (
    make_final_result,
    make_pack_context,
)


def test_execution_pipeline_accessors_and_validate_edges() -> None:
    """Cover property accessors and validate failure paths."""
    pipeline = ExecutionPipeline(auto_register=True)
    assert pipeline.registry is not None
    assert pipeline.dispatcher is not None
    assert pipeline.execution_mode is ExecutionMode.DEPENDENCY

    # Not initialized → validate false
    assert pipeline.validate() is False

    pipeline.initialize()
    assert pipeline.validate() is True

    # Force registry invalid after auto-register
    pipeline.registry.unregister_interpreter("summary_interpreter")
    assert pipeline.validate() is False
    failed = pipeline.execute(make_pack_context(result_id="fr_reg_bad"))
    assert failed.success is False
    assert "registry_invalid" in failed.messages


def test_execution_pipeline_skips_missing_registry_entries() -> None:
    """Dispatcher order entries missing from registry are skipped."""
    dispatcher = InterpreterDispatcher()
    registry = InterpreterRegistry(dispatcher=dispatcher)
    strength = StrengthInterpreter()
    strength.initialize()
    registry.register_interpreter(
        InterpreterRegistration(
            interpreter_id="strength_interpreter",
            runtime=strength,
            priority=10,
            section_type="strength",
            version="0.0.0-skeleton",
        )
    )
    # Extra dispatcher entry not in registry
    dispatcher.register("ghost_interpreter", lambda ctx: None, priority=1)

    pipeline = ExecutionPipeline(
        interpreter_registry=registry,
        dispatcher=dispatcher,
        auto_register=False,
        execution_mode=ExecutionMode.ORDERED,
    )
    pipeline.initialize()
    result = pipeline.execute(make_pack_context(result_id="fr_ghost"))
    assert result.success is True
    assert len(result.payload["sections"]) == 1


def test_section_collector_and_async_edge_paths() -> None:
    """Cover remaining collector/async/isolator branches."""
    collector = SectionCollector()
    bad_section = SectionResult(id="", section_type="")
    collected = collector.collect_from_dispatch(
        (("x", {"success": True, "section": bad_section}),)
    )
    # invalid section still collected structurally; validate fails
    assert collected.validate() is False

    # RuntimeExecuteResult-like object path
    class _Payload:
        success = True
        payload = {"interpretation_section": SectionResult(id="s1", section_type="t")}
        messages = ()

    collected2 = collector.collect_from_dispatch((("a", _Payload()),))
    assert collected2.section_ids() == ("s1",)

    # Mapping messages path + unknown failure
    collected3 = collector.collect_from_dispatch(
        (
            ("b", {"success": False, "messages": ()}),
            ("c", object()),
        )
    )
    assert "b" in collected3.failed_interpreter_ids

    isolator = ErrorIsolator()
    assert IsolatedExecutionResult(entry_id="z", success=True).validate() is True

    executor = FutureAsyncExecutor()
    invalid_plan = AsyncExecutionPlan(mode="nope")  # type: ignore[arg-type]
    assert invalid_plan.validate() is False
    assert executor.execute(invalid_plan, {"a": lambda: 1}) == ()

    # Missing callback ids are skipped
    plan = AsyncExecutionPlan(mode=ExecutionMode.ORDERED, entry_ids=("a", "missing"))
    results = executor.execute(plan, {"a": lambda: 1})
    assert len(results) == 1
