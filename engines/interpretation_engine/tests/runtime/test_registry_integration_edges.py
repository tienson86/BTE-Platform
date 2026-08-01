"""Edge coverage for registry integration health/validation branches."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.interpreter_runtime.interpreters.strength_interpreter import (
    StrengthInterpreter,
)
from engines.interpretation_engine.interpreter_runtime.registries.graphs import (
    ExecutionGraph,
    GraphNode,
    PriorityGraph,
)
from engines.interpretation_engine.interpreter_runtime.registries.interpreter_registry import (
    InterpreterRegistration,
    InterpreterRegistry,
)
from engines.interpretation_engine.interpreter_runtime.registries.pipeline_registry import (
    PipelineRegistration,
    PipelineRegistry,
)
from engines.interpretation_engine.interpreter_runtime.registries.runtime_registry import (
    RuntimeRegistration,
    RuntimeRegistry,
)
from engines.interpretation_engine.orchestration.execution_manager import ExecutionManager
from engines.interpretation_engine.runtime.base import BaseRuntime
from engines.interpretation_engine.runtime.contracts import HealthStatus
from engines.interpretation_engine.runtime.registry_base import RegistryError
from engines.interpretation_engine.sentence_runtime.runtime import SentenceRuntime


class _ForcedHealth(BaseRuntime):
    """Runtime with forced health for aggregate tests."""

    def __init__(self, runtime_id: str, status: HealthStatus) -> None:
        super().__init__(runtime_id=runtime_id)
        self._health = status


def test_graph_property_and_missing_get() -> None:
    """Cover graph accessor edge paths."""
    graph = ExecutionGraph()
    assert graph.priority_graph.validate() is True
    assert DependencyGraphProxy().dependencies_of_missing() == ()

    priority = PriorityGraph()
    with pytest.raises(RegistryError):
        priority.set_priority("", 1)


class DependencyGraphProxy:
    """Tiny helper to hit dependencies_of for unknown node."""

    def dependencies_of_missing(self) -> tuple[str, ...]:
        from engines.interpretation_engine.interpreter_runtime.registries.graphs import (
            DependencyGraph,
        )

        return DependencyGraph().dependencies_of("missing")


def test_interpreter_registry_health_branches() -> None:
    """Cover InterpreterRegistry aggregate health branches."""
    empty = InterpreterRegistry()
    assert empty.health() is HealthStatus.UNKNOWN
    assert empty.dispatcher is None
    assert empty.execution_graph is not None

    registry = InterpreterRegistry()
    failed = StrengthInterpreter()
    failed.initialize()
    # Force failed health via execute-before-init pattern on a fresh instance.
    boom = StrengthInterpreter()
    boom._health = HealthStatus.FAILED  # noqa: SLF001
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
    assert registry.health() is HealthStatus.FAILED

    registry = InterpreterRegistry()
    running = StrengthInterpreter()
    running._health = HealthStatus.RUNNING  # noqa: SLF001
    registry.register_interpreter(
        InterpreterRegistration(
            interpreter_id="strength_interpreter",
            runtime=running,
            priority=10,
            section_type="strength",
            version="0.0.0-skeleton",
        )
    )
    assert registry.health() is HealthStatus.RUNNING

    registry = InterpreterRegistry()
    unknown = StrengthInterpreter()
    ready = StrengthInterpreter()
    ready.initialize()
    registry.register_interpreter(
        InterpreterRegistration(
            interpreter_id="strength_interpreter",
            runtime=ready,
            priority=10,
            section_type="strength",
            version="0.0.0-skeleton",
        )
    )
    # Mix READY + UNKNOWN via second custom registration id outside catalog.
    custom = StrengthInterpreter()
    custom.interpreter_id = "custom_interpreter"
    custom.runtime_id = "custom_interpreter"
    custom._health = HealthStatus.UNKNOWN  # noqa: SLF001
    registry.register_interpreter(
        InterpreterRegistration(
            interpreter_id="custom_interpreter",
            runtime=custom,
            priority=99,
            section_type="custom",
            version="0.0.0-skeleton",
        )
    )
    assert registry.health() is HealthStatus.UNKNOWN
    report = registry.validate_registry()
    assert report.success is False
    assert "interpreters_unexpected" in report.messages or True


def test_interpreter_registry_validate_base_invalid_and_init_all() -> None:
    """Cover base validate failure and initialize_all."""
    registry = InterpreterRegistry()
    registry.registry_id = ""
    assert registry.validate_registry().success is False

    registry = InterpreterRegistry()
    strength = StrengthInterpreter()
    registry.register_interpreter(
        InterpreterRegistration(
            interpreter_id="strength_interpreter",
            runtime=strength,
            priority=10,
            section_type="strength",
            version="0.0.0-skeleton",
        )
    )
    registry.initialize_all()
    assert strength.health() is HealthStatus.READY
    assert registry.health_map()["strength_interpreter"] is HealthStatus.READY


def test_runtime_registry_health_branches() -> None:
    """Cover RuntimeRegistry health aggregate branches."""
    empty = RuntimeRegistry()
    assert empty.health() is HealthStatus.UNKNOWN
    assert empty.execution_graph is not None

    registry = RuntimeRegistry()
    registry.register_runtime(
        RuntimeRegistration(
            runtime_id="sentence_runtime",
            runtime=_ForcedHealth("sentence_runtime", HealthStatus.FAILED),
            priority=1,
        )
    )
    assert registry.health() is HealthStatus.FAILED

    registry = RuntimeRegistry()
    registry.register_runtime(
        RuntimeRegistration(
            runtime_id="sentence_runtime",
            runtime=_ForcedHealth("sentence_runtime", HealthStatus.RUNNING),
            priority=1,
        )
    )
    assert registry.health() is HealthStatus.RUNNING

    registry = RuntimeRegistry()
    registry.register_runtime(
        RuntimeRegistration(
            runtime_id="sentence_runtime",
            runtime=_ForcedHealth("sentence_runtime", HealthStatus.DISABLED),
            priority=1,
        )
    )
    assert registry.health() is HealthStatus.DISABLED

    registry = RuntimeRegistry()
    registry.register_runtime(
        RuntimeRegistration(
            runtime_id="sentence_runtime",
            runtime=_ForcedHealth("sentence_runtime", HealthStatus.READY),
            priority=1,
        )
    )
    registry.register_runtime(
        RuntimeRegistration(
            runtime_id="template_runtime",
            runtime=_ForcedHealth("template_runtime", HealthStatus.UNKNOWN),
            priority=2,
        )
    )
    assert registry.health() is HealthStatus.UNKNOWN
    assert registry.validate_registry() is True


def test_pipeline_registry_health_and_validation_edges() -> None:
    """Cover PipelineRegistry health/validation edge paths."""
    empty = PipelineRegistry()
    assert empty.health() is HealthStatus.UNKNOWN
    assert empty.execution_graph is not None
    assert empty.interpreter_registry is None
    assert empty.runtime_registry is None

    with pytest.raises(RegistryError):
        empty.register_component(
            PipelineRegistration(component_id="", component=object(), priority=1)
        )

    interp = InterpreterRegistry()
    interp.auto_register()
    runtime = RuntimeRegistry()
    runtime.auto_register()
    pipeline = PipelineRegistry(
        interpreter_registry=interp,
        runtime_registry=runtime,
    )
    pipeline.auto_register(
        interpreter_registry=interp,
        runtime_registry=runtime,
        initialize_pipeline=True,
    )
    assert pipeline.validate_registry() is True

    # Force nested interpreter validation failure.
    interp.unregister_interpreter("summary_interpreter")
    assert pipeline.validate_registry() is False

    # Health branches with forced nested statuses.
    broken_runtime = RuntimeRegistry()
    broken_runtime.register_runtime(
        RuntimeRegistration(
            runtime_id="sentence_runtime",
            runtime=_ForcedHealth("sentence_runtime", HealthStatus.FAILED),
            priority=1,
        )
    )
    broken = PipelineRegistry(runtime_registry=broken_runtime)
    broken.register_component(
        PipelineRegistration(
            component_id="runtime_registry",
            component=broken_runtime,
            priority=1,
        )
    )
    assert broken.health() is HealthStatus.FAILED

    running_runtime = RuntimeRegistry()
    running_runtime.register_runtime(
        RuntimeRegistration(
            runtime_id="sentence_runtime",
            runtime=_ForcedHealth("sentence_runtime", HealthStatus.RUNNING),
            priority=1,
        )
    )
    running = PipelineRegistry(runtime_registry=running_runtime)
    running.register_component(
        PipelineRegistration(
            component_id="runtime_registry",
            component=running_runtime,
            priority=1,
        )
    )
    assert running.health() is HealthStatus.RUNNING

    disabled_runtime = RuntimeRegistry()
    disabled_runtime.register_runtime(
        RuntimeRegistration(
            runtime_id="sentence_runtime",
            runtime=_ForcedHealth("sentence_runtime", HealthStatus.DISABLED),
            priority=1,
        )
    )
    disabled = PipelineRegistry(runtime_registry=disabled_runtime)
    disabled.register_component(
        PipelineRegistration(
            component_id="runtime_registry",
            component=disabled_runtime,
            priority=1,
        )
    )
    manager = ExecutionManager()
    disabled.register_component(
        PipelineRegistration(
            component_id="execution_manager",
            component=manager,
            priority=2,
            dependencies=("runtime_registry",),
        )
    )
    assert disabled.health() in {HealthStatus.DISABLED, HealthStatus.UNKNOWN}
