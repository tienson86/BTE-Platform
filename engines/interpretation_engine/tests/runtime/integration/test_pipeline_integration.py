"""Pipeline-focused integration tests."""

from __future__ import annotations

from engines.interpretation_engine.events import LocalEventBus
from engines.interpretation_engine.monitoring import RuntimeMonitor
from engines.interpretation_engine.orchestration import (
    ExecutionManager,
    ExecutionPipeline,
    RuntimePipeline,
)
from engines.interpretation_engine.orchestration.async_executor import ExecutionMode
from engines.interpretation_engine.runtime.contracts import HealthStatus
from engines.interpretation_engine.tests.runtime.conftest import make_pack_context


def test_execution_pipeline_modes_integration() -> None:
    """ExecutionPipeline works for dependency/ordered/future_async modes."""
    for mode in (
        ExecutionMode.DEPENDENCY,
        ExecutionMode.ORDERED,
        ExecutionMode.FUTURE_ASYNC,
    ):
        pipeline = ExecutionPipeline(
            execution_mode=mode,
            event_bus=LocalEventBus(bus_id=f"bus_{mode.value}"),
            monitor=RuntimeMonitor(monitor_id=f"mon_{mode.value}"),
        )
        pipeline.initialize()
        result = pipeline.execute(make_pack_context(result_id=f"fr_{mode.value}"))
        assert result.success is True
        assert result.payload["execution_mode"] == mode.value
        assert len(result.payload["sections"]) == 12
        pipeline.shutdown()


def test_runtime_pipeline_and_execution_manager_integration() -> None:
    """Stage RuntimePipeline + ExecutionManager remain integrable."""
    pipeline = RuntimePipeline()
    manager = ExecutionManager(pipeline)
    manager.initialize()
    assert manager.validate() is True
    result = manager.execute(make_pack_context(result_id="fr_runtime_pipe"))
    assert result.success is True
    assert "interpretation_result" in result.payload
    assert manager.health() is HealthStatus.READY
    manager.shutdown()
    assert manager.health() is HealthStatus.DISABLED
