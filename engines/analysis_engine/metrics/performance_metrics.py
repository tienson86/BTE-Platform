"""Performance metrics infrastructure."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.metrics._time import Stopwatch


@dataclass(frozen=True, slots=True)
class TimingSample:
    """Single named timing sample."""

    name: str
    duration_ms: float
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PerformanceMetricsSnapshot:
    """Immutable snapshot of performance timings."""

    total_duration_ms: float
    sample_count: int
    avg_duration_ms: float | None
    min_duration_ms: float | None
    max_duration_ms: float | None
    samples: tuple[TimingSample, ...] = ()
    counters: Mapping[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible dictionary representation."""
        return {
            "total_duration_ms": self.total_duration_ms,
            "sample_count": self.sample_count,
            "avg_duration_ms": self.avg_duration_ms,
            "min_duration_ms": self.min_duration_ms,
            "max_duration_ms": self.max_duration_ms,
            "samples": [
                {
                    "name": sample.name,
                    "duration_ms": sample.duration_ms,
                    "metadata": dict(sample.metadata),
                }
                for sample in self.samples
            ],
            "counters": dict(self.counters),
        }


class PerformanceMetrics:
    """Collect named timing samples and simple performance counters.

    Infrastructure only. Distinct from ``runtime.models.PerformanceMetrics``.
    No dashboard rendering.
    """

    def __init__(self) -> None:
        """Initialize an empty performance metrics collector."""
        self._samples: list[TimingSample] = []
        self._counters: dict[str, int] = {}
        self._active: dict[str, Stopwatch] = {}
        self._total_duration_ms = 0.0

    def start_timer(self, name: str) -> None:
        """Start a named timer."""
        watch = Stopwatch()
        watch.start()
        self._active[name] = watch

    def stop_timer(
        self,
        name: str,
        *,
        metadata: Mapping[str, Any] | None = None,
    ) -> float:
        """Stop a named timer and record a sample. Return duration ms."""
        watch = self._active.pop(name, None)
        if watch is None:
            duration = 0.0
        else:
            duration = watch.stop()
        self.record_timing(name, duration, metadata=metadata)
        return duration

    def record_timing(
        self,
        name: str,
        duration_ms: float,
        *,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        """Record an explicit timing sample."""
        sample = TimingSample(
            name=name,
            duration_ms=float(duration_ms),
            metadata=dict(metadata or {}),
        )
        self._samples.append(sample)
        self._total_duration_ms += float(duration_ms)

    def increment(self, counter: str, amount: int = 1) -> None:
        """Increment a named counter."""
        self._counters[counter] = self._counters.get(counter, 0) + amount

    def snapshot(self) -> PerformanceMetricsSnapshot:
        """Return an immutable performance metrics snapshot."""
        durations = tuple(sample.duration_ms for sample in self._samples)
        if durations:
            avg = sum(durations) / len(durations)
            minimum = min(durations)
            maximum = max(durations)
        else:
            avg = None
            minimum = None
            maximum = None
        return PerformanceMetricsSnapshot(
            total_duration_ms=self._total_duration_ms,
            sample_count=len(self._samples),
            avg_duration_ms=avg,
            min_duration_ms=minimum,
            max_duration_ms=maximum,
            samples=tuple(self._samples),
            counters=dict(self._counters),
        )

    def reset(self) -> None:
        """Clear all collected performance metrics."""
        self._samples.clear()
        self._counters.clear()
        self._active.clear()
        self._total_duration_ms = 0.0
