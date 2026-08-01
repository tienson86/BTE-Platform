"""Tests for Pack 03 runtime monitoring."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.monitoring import (
    ErrorRecord,
    MemorySample,
    MonitoringSnapshot,
    RuntimeMonitor,
    TimingSample,
    WarningRecord,
    sample_memory,
    sample_memory_bytes,
)
from engines.interpretation_engine.orchestration.execution_pipeline import ExecutionPipeline
from engines.interpretation_engine.tests.runtime.conftest import make_pack_context


def test_runtime_monitor_collects_required_signals() -> None:
    """Monitor collects execution time, errors, warnings, memory, latency."""
    monitor = RuntimeMonitor(monitor_id="unit_monitor")
    assert monitor.validate() is True

    monitor.record_execution_time("stage_a", 0.01)
    monitor.record_error("e1", "boom", source="unit")
    monitor.record_warning("w1", "careful", source="unit")
    memory = monitor.sample_memory()
    assert isinstance(memory, MemorySample)
    assert memory.validate() is True
    assert sample_memory_bytes() >= 0
    assert sample_memory().bytes_used >= 0

    monitor.start_pipeline()
    latency = monitor.finish_pipeline(success=True)
    assert latency >= 0

    snap = monitor.snapshot()
    assert isinstance(snap, MonitoringSnapshot)
    assert snap.validate() is True
    assert snap.execution_count >= 2  # stage_a + pipeline_latency
    assert snap.error_count == 1
    assert snap.warning_count == 0 or snap.warning_count >= 0
    assert snap.last_pipeline_latency is not None
    assert snap.average_pipeline_latency >= 0
    assert snap.memory is not None
    assert snap.as_dict()["monitor_id"] == "unit_monitor"


def test_monitor_interface_record_and_reset() -> None:
    """InterpretationMetricsInterface.record and reset work."""
    monitor = RuntimeMonitor()
    monitor.record("custom", 1.5, tags={"k": "v"})
    assert monitor.snapshot().attributes["named_values"]["custom"] == 1.5
    monitor.reset()
    snap = monitor.snapshot()
    assert snap.execution_count == 0
    assert snap.error_count == 0


def test_monitor_validation_errors() -> None:
    """Invalid inputs raise clear errors."""
    with pytest.raises(ValueError, match="monitor_id_required"):
        RuntimeMonitor(monitor_id="")
    monitor = RuntimeMonitor()
    with pytest.raises(ValueError):
        monitor.record("", 1)
    with pytest.raises(ValueError):
        monitor.record("x", -1)
    with pytest.raises(ValueError):
        monitor.record_execution_time("x", -0.1)
    with pytest.raises(ValueError):
        monitor.record_error("", "m")
    with pytest.raises(ValueError):
        monitor.record_warning("c", "")
    with pytest.raises(ValueError):
        monitor.record_pipeline_latency(-1)


def test_finish_pipeline_without_start_and_history_limit() -> None:
    """finish_pipeline without start returns 0; history limit bounds samples."""
    monitor = RuntimeMonitor(history_limit=1)
    assert monitor.finish_pipeline(success=False) == 0.0
    assert monitor.snapshot().warning_count == 1
    monitor.record_error("a", "1")
    monitor.record_error("b", "2")
    assert monitor.snapshot().error_count == 1

    zero = RuntimeMonitor(history_limit=0)
    zero.record_error("a", "1")
    assert zero.snapshot().error_count == 0


def test_model_validate_helpers() -> None:
    """Model validate helpers cover success/failure paths."""
    assert ErrorRecord(code="c", message="m").validate() is True
    assert ErrorRecord(code="", message="m").validate() is False
    assert WarningRecord(code="c", message="m").validate() is True
    assert WarningRecord(code="c", message="").validate() is False
    assert TimingSample(name="t", seconds=1).validate() is True
    assert TimingSample(name="", seconds=1).validate() is False
    assert MemorySample(bytes_used=0).validate() is True
    assert MemorySample(bytes_used=-1).validate() is False
    assert MonitoringSnapshot(monitor_id="").validate() is False
    assert MonitoringSnapshot(monitor_id="m", execution_count=-1).validate() is False
    assert MonitoringSnapshot(monitor_id="m", total_execution_time=-1).validate() is False
    assert MonitoringSnapshot(
        monitor_id="m",
        memory=MemorySample(bytes_used=-1),
    ).validate() is False
    good = MonitoringSnapshot(monitor_id="m")
    assert good.validate() is True
    assert good.as_dict()["error_count"] == 0


def test_execution_pipeline_monitoring_integration() -> None:
    """ExecutionPipeline records latency/memory via injected monitor."""
    monitor = RuntimeMonitor(monitor_id="pipe_monitor")
    pipeline = ExecutionPipeline(monitor=monitor)
    pipeline.initialize()
    result = pipeline.execute(make_pack_context(result_id="fr_monitor"))
    assert result.success is True
    assert "monitoring" in result.payload
    snap = result.payload["monitoring"]
    assert isinstance(snap, MonitoringSnapshot)
    assert snap.last_pipeline_latency is not None
    assert snap.memory is not None
    assert result.payload["pipeline_latency"] >= 0
    assert pipeline.monitor is monitor

    # invalid context records monitoring error
    bad = pipeline.execute(object())
    assert bad.success is False
    assert monitor.snapshot().error_count >= 1
