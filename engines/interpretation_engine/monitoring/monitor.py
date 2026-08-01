"""Runtime monitoring collector for Pack 03.

Collects:
- execution time
- errors
- warnings
- memory
- pipeline latency

Local/in-process only. Dependency Injection only. No external APM.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from typing import Any, Mapping

from engines.interpretation_engine.metrics.metrics_interface import (
    InterpretationMetricsInterface,
)
from engines.interpretation_engine.monitoring.memory import sample_memory
from engines.interpretation_engine.monitoring.models import (
    ErrorRecord,
    MemorySample,
    MonitoringSnapshot,
    TimingSample,
    WarningRecord,
)

logger = logging.getLogger(__name__)


def _utc_now() -> str:
    """Return UTC ISO-8601 timestamp."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class RuntimeMonitor(InterpretationMetricsInterface):
    """In-process runtime monitor for Pack 03 infrastructure."""

    def __init__(
        self,
        *,
        monitor_id: str = "runtime_monitor",
        history_limit: int = 256,
    ) -> None:
        """Initialize an empty monitor.

        Args:
            monitor_id: Diagnostic identifier.
            history_limit: Max retained timing/error/warning samples.
        """
        if not monitor_id:
            raise ValueError("monitor_id_required")
        self.monitor_id = monitor_id
        self._history_limit = max(0, history_limit)
        self._execution_count = 0
        self._total_execution_time = 0.0
        self._last_execution_time: float | None = None
        self._pipeline_latency_total = 0.0
        self._pipeline_latency_count = 0
        self._last_pipeline_latency: float | None = None
        self._pipeline_started_at: float | None = None
        self._errors: list[ErrorRecord] = []
        self._warnings: list[WarningRecord] = []
        self._timings: list[TimingSample] = []
        self._memory: MemorySample | None = None
        self._peak_memory_bytes = 0
        self._named_values: dict[str, float] = {}

    def record(
        self,
        name: str,
        value: float,
        tags: Mapping[str, str] | None = None,
    ) -> None:
        """Record a generic metric sample (interface contract)."""
        if not name:
            raise ValueError("metric_name_required")
        if value < 0:
            raise ValueError("metric_value_invalid")
        self._named_values[name] = float(value)
        self.record_execution_time(name, float(value), attributes=dict(tags or {}))

    def record_execution_time(
        self,
        name: str,
        seconds: float,
        *,
        attributes: Mapping[str, Any] | None = None,
    ) -> None:
        """Record an execution-time sample."""
        if seconds < 0:
            raise ValueError("execution_time_invalid")
        sample = TimingSample(
            name=name,
            seconds=seconds,
            timestamp=_utc_now(),
            attributes=dict(attributes or {}),
        )
        self._append_limited(self._timings, sample)
        self._execution_count += 1
        self._total_execution_time += seconds
        self._last_execution_time = seconds
        logger.debug(
            "monitor_execution_time",
            extra={"monitor_id": self.monitor_id, "name": name, "seconds": seconds},
        )

    def record_error(
        self,
        code: str,
        message: str,
        *,
        source: str = "",
        attributes: Mapping[str, Any] | None = None,
    ) -> None:
        """Record an error."""
        if not code or not message:
            raise ValueError("error_record_invalid")
        record = ErrorRecord(
            code=code,
            message=message,
            source=source or self.monitor_id,
            timestamp=_utc_now(),
            attributes=dict(attributes or {}),
        )
        self._append_limited(self._errors, record)
        logger.warning(
            "monitor_error",
            extra={
                "monitor_id": self.monitor_id,
                "error_code": code,
                "error_detail": message,
            },
        )

    def record_warning(
        self,
        code: str,
        message: str,
        *,
        source: str = "",
        attributes: Mapping[str, Any] | None = None,
    ) -> None:
        """Record a warning."""
        if not code or not message:
            raise ValueError("warning_record_invalid")
        record = WarningRecord(
            code=code,
            message=message,
            source=source or self.monitor_id,
            timestamp=_utc_now(),
            attributes=dict(attributes or {}),
        )
        self._append_limited(self._warnings, record)
        logger.info(
            "monitor_warning",
            extra={
                "monitor_id": self.monitor_id,
                "warning_code": code,
                "warning_detail": message,
            },
        )

    def sample_memory(self) -> MemorySample:
        """Sample current process memory and update peak."""
        sample = sample_memory(source=self.monitor_id)
        self._memory = sample
        if sample.bytes_used > self._peak_memory_bytes:
            self._peak_memory_bytes = sample.bytes_used
        return sample

    def start_pipeline(self) -> None:
        """Mark pipeline start for latency measurement."""
        self._pipeline_started_at = time.perf_counter()
        self.sample_memory()

    def finish_pipeline(self, *, success: bool = True) -> float:
        """Mark pipeline finish; record latency; return elapsed seconds."""
        if self._pipeline_started_at is None:
            elapsed = 0.0
        else:
            elapsed = max(time.perf_counter() - self._pipeline_started_at, 0.0)
        self._pipeline_started_at = None
        self.record_pipeline_latency(elapsed)
        self.sample_memory()
        if not success:
            self.record_warning(
                "pipeline_unsuccessful",
                "pipeline finished with success=False",
                source=self.monitor_id,
            )
        return elapsed

    def record_pipeline_latency(self, seconds: float) -> None:
        """Record a pipeline latency sample."""
        if seconds < 0:
            raise ValueError("pipeline_latency_invalid")
        self._pipeline_latency_total += seconds
        self._pipeline_latency_count += 1
        self._last_pipeline_latency = seconds
        self.record_execution_time(
            "pipeline_latency",
            seconds,
            attributes={"kind": "pipeline_latency"},
        )

    def snapshot(self) -> MonitoringSnapshot:
        """Return an immutable monitoring snapshot."""
        average_execution = (
            self._total_execution_time / self._execution_count
            if self._execution_count
            else 0.0
        )
        average_latency = (
            self._pipeline_latency_total / self._pipeline_latency_count
            if self._pipeline_latency_count
            else 0.0
        )
        if self._memory is None:
            self.sample_memory()
        return MonitoringSnapshot(
            monitor_id=self.monitor_id,
            execution_count=self._execution_count,
            total_execution_time=self._total_execution_time,
            average_execution_time=average_execution,
            last_execution_time=self._last_execution_time,
            pipeline_latency_total=self._pipeline_latency_total,
            pipeline_latency_count=self._pipeline_latency_count,
            average_pipeline_latency=average_latency,
            last_pipeline_latency=self._last_pipeline_latency,
            error_count=len(self._errors),
            warning_count=len(self._warnings),
            errors=tuple(self._errors),
            warnings=tuple(self._warnings),
            timings=tuple(self._timings),
            memory=self._memory,
            peak_memory_bytes=self._peak_memory_bytes,
            attributes={"named_values": dict(self._named_values)},
        )

    def reset(self) -> None:
        """Reset all collected monitoring state."""
        self._execution_count = 0
        self._total_execution_time = 0.0
        self._last_execution_time = None
        self._pipeline_latency_total = 0.0
        self._pipeline_latency_count = 0
        self._last_pipeline_latency = None
        self._pipeline_started_at = None
        self._errors.clear()
        self._warnings.clear()
        self._timings.clear()
        self._memory = None
        self._peak_memory_bytes = 0
        self._named_values.clear()
        logger.info("monitor_reset", extra={"monitor_id": self.monitor_id})

    def validate(self) -> bool:
        """Validate monitor readiness."""
        return bool(self.monitor_id) and self._history_limit >= 0

    def _append_limited(self, target: list[Any], item: Any) -> None:
        """Append item to a bounded history list."""
        if self._history_limit <= 0:
            return
        target.append(item)
        overflow = len(target) - self._history_limit
        if overflow > 0:
            del target[:overflow]


# Backward-compatible alias.
Monitor = RuntimeMonitor
