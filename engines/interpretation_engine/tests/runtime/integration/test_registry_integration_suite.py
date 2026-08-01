"""Registry-focused integration tests."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.catalog import (
    INTERPRETER_SKELETON_IDS,
)
from engines.interpretation_engine.interpreter_runtime.registries import (
    InterpreterRegistry,
    PipelineRegistry,
    RuntimeRegistry,
)
from engines.interpretation_engine.runtime.contracts import HealthStatus


def test_interpreter_runtime_pipeline_registries_integration() -> None:
    """All three registries auto-register and validate together."""
    interpreters = InterpreterRegistry()
    runtimes = RuntimeRegistry()
    pipeline = PipelineRegistry(
        interpreter_registry=interpreters,
        runtime_registry=runtimes,
    )

    interpreters.auto_register()
    runtimes.auto_register()
    pipeline.auto_register(
        interpreter_registry=interpreters,
        runtime_registry=runtimes,
    )

    assert set(interpreters.list()) == set(INTERPRETER_SKELETON_IDS)
    assert interpreters.validate_registry().success is True
    assert runtimes.validate_registry() is True
    assert pipeline.validate_registry() is True
    assert interpreters.health() is HealthStatus.READY
    assert runtimes.health() is HealthStatus.READY
    assert pipeline.health() is HealthStatus.READY

    # Graph orders are deterministic and dependency-aware.
    exec_order = interpreters.execution_graph_order()
    assert exec_order.index("strength_interpreter") < exec_order.index(
        "summary_interpreter"
    )
    assert runtimes.execution_order()[0] == "interpreter_runtime"
    assert pipeline.execution_order()[-1] == "execution_manager"
