"""Execution metrics infrastructure."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.metrics._time import Stopwatch, utc_now


@dataclass(frozen=True, slots=True)
class ExecutionMetricsSnapshot:
    """Immutable snapshot of execution metrics."""

    execution_id: str
    started_at: str | None
    completed_at: str | None
    duration_ms: float | None
    attempt_count: int
    success_count: int
    failure_count: int
    status_counts: Mapping[str, int] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible dictionary representation."""
        return {
            "execution_id": self.execution_id,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_ms": self.duration_ms,
            "attempt_count": self.attempt_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "status_counts": dict(self.status_counts),
            "metadata": dict(self.metadata),
        }


class ExecutionMetrics:
    """Collect execution-level counters and timings.

    Infrastructure only. No dashboard rendering.
    """

    def __init__(self, execution_id: str) -> None:
        """Initialize metrics for a single execution."""
        self._execution_id = execution_id
        self._started_at: str | None = None
        self._completed_at: str | None = None
        self._duration_ms: float | None = None
        self._attempt_count = 0
        self._success_count = 0
        self._failure_count = 0
        self._status_counts: dict[str, int] = {}
        self._metadata: dict[str, Any] = {}
        self._stopwatch = Stopwatch()

    @property
    def execution_id(self) -> str:
        """Return the execution identifier."""
        return self._execution_id

    def start(self) -> None:
        """Mark execution start."""
        self._started_at = utc_now()
        self._stopwatch.start()

    def complete(self, *, success: bool) -> None:
        """Mark execution completion and record success/failure."""
        self._completed_at = utc_now()
        self._duration_ms = self._stopwatch.stop()
        if success:
            self._success_count += 1
            self.record_status("succeeded")
        else:
            self._failure_count += 1
            self.record_status("failed")

    def record_attempt(self) -> None:
        """Increment attempt counter."""
        self._attempt_count += 1

    def record_status(self, status: str) -> None:
        """Increment a status counter."""
        self._status_counts[status] = self._status_counts.get(status, 0) + 1

    def set_metadata(self, key: str, value: Any) -> None:
        """Store opaque metadata for the execution metrics record."""
        self._metadata[key] = value

    def snapshot(self) -> ExecutionMetricsSnapshot:
        """Return an immutable metrics snapshot."""
        return ExecutionMetricsSnapshot(
            execution_id=self._execution_id,
            started_at=self._started_at,
            completed_at=self._completed_at,
            duration_ms=self._duration_ms,
            attempt_count=self._attempt_count,
            success_count=self._success_count,
            failure_count=self._failure_count,
            status_counts=dict(self._status_counts),
            metadata=dict(self._metadata),
        )

    def reset(self) -> None:
        """Clear collected metrics while preserving execution_id."""
        self._started_at = None
        self._completed_at = None
        self._duration_ms = None
        self._attempt_count = 0
        self._success_count = 0
        self._failure_count = 0
        self._status_counts.clear()
        self._metadata.clear()
        self._stopwatch = Stopwatch()
