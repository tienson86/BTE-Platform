"""Health-focused integration tests."""

from __future__ import annotations

from engines.interpretation_engine.health import HealthManager, HealthStatus
from engines.interpretation_engine.interpreter_runtime.registries import (
    InterpreterRegistry,
    RuntimeRegistry,
)
from engines.interpretation_engine.orchestration import ExecutionPipeline
from engines.interpretation_engine.runtime.base import BaseRuntime


class _Forced(BaseRuntime):
    """Runtime with forced health for aggregate checks."""

    def __init__(self, runtime_id: str, status: HealthStatus) -> None:
        super().__init__(runtime_id=runtime_id)
        self._health = status


def test_health_manager_with_pipeline_and_registries() -> None:
    """HealthManager aggregates pipeline + registry runtime health."""
    manager = HealthManager()
    pipeline = ExecutionPipeline()
    pipeline.initialize()
    interpreters = InterpreterRegistry()
    interpreters.auto_register()
    runtimes = RuntimeRegistry()
    runtimes.auto_register()

    manager.register("pipeline", pipeline)
    manager.register("interpreters_proxy", _Forced("interpreters_proxy", interpreters.health()))
    for runtime_id in runtimes.list():
        entry = runtimes.lookup(runtime_id)
        assert entry is not None
        manager.register(runtime_id, entry.runtime)

    assert manager.validate() is True
    assert manager.overall() is HealthStatus.READY
    snapshot = manager.snapshot()
    assert snapshot["pipeline"] == "READY"
    assert snapshot["overall"] == "READY"

    manager.register("failed", _Forced("failed", HealthStatus.FAILED))
    assert manager.overall() is HealthStatus.FAILED

    pipeline.shutdown()
    interpreters.shutdown_all()
    runtimes.shutdown_all()
