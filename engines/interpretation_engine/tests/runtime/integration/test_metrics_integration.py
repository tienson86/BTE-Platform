"""Metrics-focused integration tests."""

from __future__ import annotations

from engines.interpretation_engine.metrics.runtime_metrics import RuntimeMetricsCollector
from engines.interpretation_engine.monitoring import RuntimeMonitor
from engines.interpretation_engine.orchestration import ExecutionPipeline
from engines.interpretation_engine.runtime.contracts import HealthStatus
from engines.interpretation_engine.tests.runtime.conftest import make_pack_context


def test_metrics_and_monitoring_pipeline_integration() -> None:
    """RuntimeMetricsCollector + RuntimeMonitor integrate with ExecutionPipeline."""
    monitor = RuntimeMonitor(monitor_id="metrics_integration")
    pipeline = ExecutionPipeline(monitor=monitor)
    pipeline.initialize()

    collector = RuntimeMetricsCollector()
    collector.register("execution_pipeline", pipeline)

    result = pipeline.execute(make_pack_context(result_id="fr_metrics_int"))
    assert result.success is True

    snap = collector.aggregate()
    assert snap.execution_count >= 1
    assert snap.success_count >= 1
    assert snap.health in {HealthStatus.READY, HealthStatus.RUNNING, HealthStatus.FAILED}
    as_dict = collector.as_dict()
    assert "execution_pipeline" in as_dict
    assert "aggregate" in as_dict

    monitoring = result.payload["monitoring"]
    assert monitoring.last_pipeline_latency is not None
    assert monitoring.memory is not None
    assert monitoring.execution_count >= 1

    pipeline.shutdown()
    assert collector.collect()["execution_pipeline"].health is HealthStatus.DISABLED
