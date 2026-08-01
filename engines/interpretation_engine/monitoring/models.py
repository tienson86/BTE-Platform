"""Monitoring snapshot models for Pack 03.

Infrastructure only. No BaZi logic. No external APM broker.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class ErrorRecord:
    """Immutable monitored error record."""

    code: str
    message: str
    source: str = ""
    timestamp: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate error record structural integrity."""
        return bool(self.code and self.message)


@dataclass(frozen=True, slots=True)
class WarningRecord:
    """Immutable monitored warning record."""

    code: str
    message: str
    source: str = ""
    timestamp: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate warning record structural integrity."""
        return bool(self.code and self.message)


@dataclass(frozen=True, slots=True)
class TimingSample:
    """Immutable timing sample."""

    name: str
    seconds: float
    timestamp: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate timing sample structural integrity."""
        return bool(self.name) and self.seconds >= 0


@dataclass(frozen=True, slots=True)
class MemorySample:
    """Immutable memory sample in bytes."""

    bytes_used: int
    timestamp: str = ""
    source: str = "process"
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate memory sample structural integrity."""
        return self.bytes_used >= 0


@dataclass(frozen=True, slots=True)
class MonitoringSnapshot:
    """Immutable monitoring snapshot.

    Collects execution time, errors, warnings, memory, and pipeline latency.
    """

    monitor_id: str
    execution_count: int = 0
    total_execution_time: float = 0.0
    average_execution_time: float = 0.0
    last_execution_time: float | None = None
    pipeline_latency_total: float = 0.0
    pipeline_latency_count: int = 0
    average_pipeline_latency: float = 0.0
    last_pipeline_latency: float | None = None
    error_count: int = 0
    warning_count: int = 0
    errors: tuple[ErrorRecord, ...] = ()
    warnings: tuple[WarningRecord, ...] = ()
    timings: tuple[TimingSample, ...] = ()
    memory: MemorySample | None = None
    peak_memory_bytes: int = 0
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate snapshot structural integrity."""
        if not self.monitor_id:
            return False
        if self.execution_count < 0 or self.error_count < 0 or self.warning_count < 0:
            return False
        if self.total_execution_time < 0 or self.pipeline_latency_total < 0:
            return False
        if self.memory is not None and not self.memory.validate():
            return False
        return True

    def as_dict(self) -> dict[str, Any]:
        """Return a serializable snapshot dictionary."""
        return {
            "monitor_id": self.monitor_id,
            "execution_count": self.execution_count,
            "total_execution_time": self.total_execution_time,
            "average_execution_time": self.average_execution_time,
            "last_execution_time": self.last_execution_time,
            "pipeline_latency_total": self.pipeline_latency_total,
            "pipeline_latency_count": self.pipeline_latency_count,
            "average_pipeline_latency": self.average_pipeline_latency,
            "last_pipeline_latency": self.last_pipeline_latency,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "errors": [
                {
                    "code": item.code,
                    "message": item.message,
                    "source": item.source,
                    "timestamp": item.timestamp,
                }
                for item in self.errors
            ],
            "warnings": [
                {
                    "code": item.code,
                    "message": item.message,
                    "source": item.source,
                    "timestamp": item.timestamp,
                }
                for item in self.warnings
            ],
            "memory_bytes": None if self.memory is None else self.memory.bytes_used,
            "peak_memory_bytes": self.peak_memory_bytes,
        }
