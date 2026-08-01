"""Additional coverage tests for Pack 03 runtime edge paths."""

from __future__ import annotations

from typing import Any

import pytest

from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.explanation_runtime.runtime import ExplanationRuntime
from engines.interpretation_engine.health.health_manager import HealthManager
from engines.interpretation_engine.interpreter_runtime.dispatcher import (
    InterpreterDispatcher,
)
from engines.interpretation_engine.interpreter_runtime.runtime import InterpreterRuntime
from engines.interpretation_engine.metrics.runtime_metrics import RuntimeMetricsCollector
from engines.interpretation_engine.orchestration.execution_manager import ExecutionManager
from engines.interpretation_engine.orchestration.runtime_pipeline import RuntimePipeline
from engines.interpretation_engine.placeholder_runtime.runtime import PlaceholderRuntime
from engines.interpretation_engine.runtime.base import BaseRuntime
from engines.interpretation_engine.runtime.contracts import (
    HealthStatus,
    RuntimeExecuteResult,
    RuntimeMetricsSnapshot,
)
from engines.interpretation_engine.sentence_runtime.runtime import SentenceRuntime
from engines.interpretation_engine.template_runtime.runtime import TemplateRuntime
from engines.interpretation_engine.tests.runtime.conftest import (
    make_final_result,
    make_pack_context,
)
from engines.interpretation_engine.validation.runtime_validator import RuntimeValidator


class _BoomRuntime(BaseRuntime):
    """Runtime that raises inside execute body."""

    def __init__(self) -> None:
        super().__init__(runtime_id="boom")

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        raise RuntimeError("boom")


class _FailingStage(BaseRuntime):
    """Stage that always fails execute body."""

    def __init__(self, runtime_id: str = "failing_stage") -> None:
        super().__init__(runtime_id=runtime_id)

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        return RuntimeExecuteResult(
            runtime_id=self.runtime_id,
            success=False,
            messages=("forced_failure",),
        )


class _ForcedHealthRuntime(BaseRuntime):
    """Runtime with mutable forced health for aggregate tests."""

    def __init__(self, runtime_id: str, status: HealthStatus) -> None:
        super().__init__(runtime_id=runtime_id)
        self._health = status


def test_base_runtime_exception_and_default_body() -> None:
    """BaseRuntime catches exceptions and default body succeeds."""
    boom = _BoomRuntime()
    boom.initialize()
    result = boom.execute(make_pack_context())
    assert result.success is False
    assert boom.health() is HealthStatus.FAILED
    assert any("runtime_execute_error" in msg for msg in result.messages)

    plain = BaseRuntime(runtime_id="plain")
    plain.initialize()
    ok = plain.execute(make_pack_context())
    assert ok.success is True
    assert "runtime_noop_success" in ok.messages

    empty = BaseRuntime(runtime_id="")
    empty.initialize()
    assert empty.validate() is False


def test_invalid_context_and_registry_accessors() -> None:
    """Cover invalid PackInterpretationContext and registry/dispatcher accessors."""
    final = make_final_result(result_id="fr_bad")
    invalid = PackInterpretationContext(
        id="",
        version="1.0.0",
        pipeline_id="p",
        source_final_result_id=final.id,
        final_result=final,
        created_at="2026-01-01T00:00:00Z",
    )
    assert invalid.validate() is False

    for runtime in (
        InterpreterRuntime(),
        SentenceRuntime(),
        TemplateRuntime(),
        PlaceholderRuntime(),
        ExplanationRuntime(),
    ):
        runtime.initialize()
        assert runtime.registry is not None
        bad = runtime.execute(invalid)
        assert bad.success is False
        assert "pack_interpretation_context_invalid" in bad.messages
        wrong_type = runtime.execute(object())
        assert wrong_type.success is False
        assert "pack_interpretation_context_required" in wrong_type.messages

    interpreter = InterpreterRuntime()
    interpreter.initialize()
    assert isinstance(interpreter.dispatcher, InterpreterDispatcher)


def test_interpreter_validate_dispatcher_failure() -> None:
    """Interpreter validate fails when dispatcher has circular deps."""
    dispatcher = InterpreterDispatcher()
    dispatcher.register("a", lambda ctx: "a", dependencies=("b",))
    dispatcher.register("b", lambda ctx: "b", dependencies=("a",))
    runtime = InterpreterRuntime(dispatcher=dispatcher)
    runtime.initialize()
    assert runtime.validate() is False


def test_pipeline_stage_failure_and_manager_property() -> None:
    """Pipeline stops on stage failure; ExecutionManager exposes pipeline."""
    failing = _FailingStage(runtime_id="interpreter_runtime")
    pipeline = RuntimePipeline(interpreter_runtime=failing)  # type: ignore[arg-type]
    # Replace first stage after construction via direct assignment workaround:
    pipeline = RuntimePipeline()
    pipeline._stages = (  # noqa: SLF001 - test injection
        _FailingStage(runtime_id="interpreter_runtime"),
        pipeline._stages[1],
        pipeline._stages[2],
        pipeline._stages[3],
        pipeline._stages[4],
    )
    pipeline.initialize()
    result = pipeline.execute(make_pack_context())
    assert result.success is False
    assert "runtime_pipeline_failed" in result.messages
    assert result.payload["failed_stage"] == "interpreter_runtime"

    uninit = RuntimePipeline()
    assert uninit.validate() is False

    manager = ExecutionManager(pipeline=RuntimePipeline())
    assert manager.pipeline.runtime_id == "runtime_pipeline"


def test_health_and_metrics_aggregate_branches() -> None:
    """Cover FAILED/RUNNING/DISABLED aggregate health branches."""
    health = HealthManager()
    health.register("failed", _ForcedHealthRuntime("failed", HealthStatus.FAILED))
    assert health.overall() is HealthStatus.FAILED

    health = HealthManager()
    health.register("running", _ForcedHealthRuntime("running", HealthStatus.RUNNING))
    assert health.overall() is HealthStatus.RUNNING
    assert health.validate() is True

    health = HealthManager()
    health.register("d1", _ForcedHealthRuntime("d1", HealthStatus.DISABLED))
    health.register("d2", _ForcedHealthRuntime("d2", HealthStatus.DISABLED))
    assert health.overall() is HealthStatus.DISABLED

    health = HealthManager()
    health.register("ready", _ForcedHealthRuntime("ready", HealthStatus.READY))
    health.register("disabled", _ForcedHealthRuntime("disabled", HealthStatus.DISABLED))
    assert health.overall() is HealthStatus.READY

    collector = RuntimeMetricsCollector()
    collector.register("failed", _ForcedHealthRuntime("failed", HealthStatus.FAILED))
    assert collector.aggregate().health is HealthStatus.FAILED
    collector = RuntimeMetricsCollector()
    collector.register("running", _ForcedHealthRuntime("running", HealthStatus.RUNNING))
    assert collector.aggregate().health is HealthStatus.RUNNING
    collector = RuntimeMetricsCollector()
    collector.register("d1", _ForcedHealthRuntime("d1", HealthStatus.DISABLED))
    assert collector.aggregate().health is HealthStatus.DISABLED
    collector = RuntimeMetricsCollector()
    collector.register("ready", _ForcedHealthRuntime("ready", HealthStatus.READY))
    collector.register("unknown", _ForcedHealthRuntime("unknown", HealthStatus.UNKNOWN))
    assert collector.aggregate().health is HealthStatus.UNKNOWN


def test_validator_edge_cases() -> None:
    """Cover validator None registry and metrics invalid paths."""
    validator = RuntimeValidator()
    assert validator.validate_registry(None).success is False  # type: ignore[arg-type]

    class _BadMetrics(BaseRuntime):
        def __init__(self) -> None:
            super().__init__(runtime_id="bad_metrics")

        def metrics(self) -> RuntimeMetricsSnapshot:
            return RuntimeMetricsSnapshot(execution_count=-1)

    bad = _BadMetrics()
    bad.initialize()
    assert validator.validate_runtime_state(bad).success is False

    class _BrokenValidate(BaseRuntime):
        def __init__(self) -> None:
            super().__init__(runtime_id="broken")

        def validate(self) -> bool:
            raise ValueError("broken")

    broken = _BrokenValidate()
    report = validator.validate_contract(broken)
    assert report.success is False
    assert any("contract_validate_error" in msg for msg in report.messages)

    assert RuntimeMetricsSnapshot(execution_time=-1).validate() is False
    assert RuntimeMetricsSnapshot(average_time=-1).validate() is False
    assert RuntimeExecuteResult(runtime_id="").validate() is False
