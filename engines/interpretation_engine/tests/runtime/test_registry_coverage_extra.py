"""Additional registry coverage branches."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.strength_interpreter import (
    StrengthInterpreter,
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
from engines.interpretation_engine.runtime.base import BaseRuntime
from engines.interpretation_engine.runtime.contracts import HealthStatus
from engines.interpretation_engine.sentence_runtime.runtime import SentenceRuntime


class _ForcedHealth(BaseRuntime):
    """Runtime with forced health."""

    def __init__(self, runtime_id: str, status: HealthStatus) -> None:
        super().__init__(runtime_id=runtime_id)
        self._health = status


def test_remaining_coverage_branches() -> None:
    """Cover remaining registry branch lines."""
    bad = InterpreterRegistration(
        interpreter_id="",
        runtime=StrengthInterpreter(),
        priority=1,
    )
    assert bad.validate() is False

    registry = InterpreterRegistry()
    injected = StrengthInterpreter()
    regs = registry.auto_register(skeletons=(injected,), initialize=False)
    assert len(regs) == 1
    assert injected.health() is HealthStatus.UNKNOWN
    assert registry.dependency_graph_order()

    assert RuntimeRegistration(
        runtime_id="",
        runtime=SentenceRuntime(),
        priority=1,
    ).validate() is False

    rr = RuntimeRegistry(
        dependencies={
            "sentence_runtime": ("template_runtime",),
            "template_runtime": ("sentence_runtime",),
        }
    )
    rr.register_runtime(
        RuntimeRegistration(
            runtime_id="sentence_runtime",
            runtime=_ForcedHealth("sentence_runtime", HealthStatus.READY),
            priority=1,
            dependencies=("template_runtime",),
        )
    )
    rr.register_runtime(
        RuntimeRegistration(
            runtime_id="template_runtime",
            runtime=_ForcedHealth("template_runtime", HealthStatus.DISABLED),
            priority=2,
            dependencies=("sentence_runtime",),
        )
    )
    assert rr.health() is HealthStatus.READY
    assert rr.priority_order() == ("sentence_runtime", "template_runtime")

    mixed = RuntimeRegistry()
    mixed.register_runtime(
        RuntimeRegistration(
            runtime_id="sentence_runtime",
            runtime=_ForcedHealth("sentence_runtime", HealthStatus.READY),
            priority=1,
        )
    )
    mixed.register_runtime(
        RuntimeRegistration(
            runtime_id="template_runtime",
            runtime=_ForcedHealth("template_runtime", HealthStatus.DISABLED),
            priority=2,
        )
    )
    pipe = PipelineRegistry()
    pipe.register_component(
        PipelineRegistration(
            component_id="runtime_registry",
            component=mixed,
            priority=20,
        )
    )
    pipe._runtime_registry = mixed  # noqa: SLF001
    assert pipe.priority_order() == ("runtime_registry",)
    assert pipe.execution_order() == ("runtime_registry",)
    assert pipe.health() is HealthStatus.READY

    disabled_reg = InterpreterRegistry()
    d1 = StrengthInterpreter()
    d1._health = HealthStatus.DISABLED  # noqa: SLF001
    disabled_reg.register_interpreter(
        InterpreterRegistration(
            interpreter_id="strength_interpreter",
            runtime=d1,
            priority=10,
            section_type="strength",
            version="0.0.0-skeleton",
        )
    )
    assert disabled_reg.health() is HealthStatus.DISABLED

    cyclic = InterpreterRegistry(
        dependencies={
            "strength_interpreter": ("season_interpreter",),
            "season_interpreter": ("strength_interpreter",),
        }
    )
    s1 = StrengthInterpreter()
    s1.initialize()
    s2 = StrengthInterpreter()
    s2.interpreter_id = "season_interpreter"
    s2.runtime_id = "season_interpreter"
    s2.initialize()
    cyclic.register_interpreter(
        InterpreterRegistration(
            interpreter_id="strength_interpreter",
            runtime=s1,
            priority=10,
            dependencies=("season_interpreter",),
            section_type="strength",
            version="0.0.0-skeleton",
        )
    )
    cyclic.register_interpreter(
        InterpreterRegistration(
            interpreter_id="season_interpreter",
            runtime=s2,
            priority=20,
            dependencies=("strength_interpreter",),
            section_type="season",
            version="0.0.0-skeleton",
        )
    )
    assert "execution_graph_invalid" in cyclic.validate_registry().messages
    cyclic.initialize_all()
