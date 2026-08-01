"""Pipeline metrics infrastructure."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.metrics._time import Stopwatch, utc_now


@dataclass(frozen=True, slots=True)
class StageMetricRecord:
    """Single stage metric sample within a pipeline run."""

    stage_id: str
    duration_ms: float
    success: bool
    attempt: int = 1
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PipelineMetricsSnapshot:
    """Immutable snapshot of pipeline metrics."""

    pipeline_id: str
    run_count: int
    success_count: int
    failure_count: int
    stage_success_counts: Mapping[str, int]
    stage_failure_counts: Mapping[str, int]
    stage_records: tuple[StageMetricRecord, ...]
    total_stage_duration_ms: float
    started_at: str | None = None
    completed_at: str | None = None
    duration_ms: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible dictionary representation."""
        return {
            "pipeline_id": self.pipeline_id,
            "run_count": self.run_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "stage_success_counts": dict(self.stage_success_counts),
            "stage_failure_counts": dict(self.stage_failure_counts),
            "stage_records": [
                {
                    "stage_id": record.stage_id,
                    "duration_ms": record.duration_ms,
                    "success": record.success,
                    "attempt": record.attempt,
                    "metadata": dict(record.metadata),
                }
                for record in self.stage_records
            ],
            "total_stage_duration_ms": self.total_stage_duration_ms,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_ms": self.duration_ms,
        }


class PipelineMetrics:
    """Collect pipeline and stage execution counters/timings.

    Infrastructure only. No orchestration logic and no dashboards.
    """

    def __init__(self, pipeline_id: str) -> None:
        """Initialize metrics for a pipeline identity."""
        self._pipeline_id = pipeline_id
        self._run_count = 0
        self._success_count = 0
        self._failure_count = 0
        self._stage_success_counts: dict[str, int] = {}
        self._stage_failure_counts: dict[str, int] = {}
        self._stage_records: list[StageMetricRecord] = []
        self._total_stage_duration_ms = 0.0
        self._started_at: str | None = None
        self._completed_at: str | None = None
        self._duration_ms: float | None = None
        self._stopwatch = Stopwatch()
        self._stage_watches: dict[str, Stopwatch] = {}

    @property
    def pipeline_id(self) -> str:
        """Return the pipeline identifier."""
        return self._pipeline_id

    def start_run(self) -> None:
        """Mark the start of a pipeline run."""
        self._run_count += 1
        self._started_at = utc_now()
        self._completed_at = None
        self._duration_ms = None
        self._stopwatch.start()

    def complete_run(self, *, success: bool) -> None:
        """Mark the completion of a pipeline run."""
        self._completed_at = utc_now()
        self._duration_ms = self._stopwatch.stop()
        if success:
            self._success_count += 1
        else:
            self._failure_count += 1

    def start_stage(self, stage_id: str) -> None:
        """Start timing a stage."""
        watch = Stopwatch()
        watch.start()
        self._stage_watches[stage_id] = watch

    def complete_stage(
        self,
        stage_id: str,
        *,
        success: bool,
        attempt: int = 1,
        duration_ms: float | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        """Complete a stage timing/counter record."""
        if duration_ms is None:
            watch = self._stage_watches.pop(stage_id, None)
            duration_ms = watch.stop() if watch is not None else 0.0
        else:
            self._stage_watches.pop(stage_id, None)
        record = StageMetricRecord(
            stage_id=stage_id,
            duration_ms=float(duration_ms),
            success=success,
            attempt=attempt,
            metadata=dict(metadata or {}),
        )
        self._stage_records.append(record)
        self._total_stage_duration_ms += float(duration_ms)
        if success:
            self._stage_success_counts[stage_id] = (
                self._stage_success_counts.get(stage_id, 0) + 1
            )
        else:
            self._stage_failure_counts[stage_id] = (
                self._stage_failure_counts.get(stage_id, 0) + 1
            )

    def snapshot(self) -> PipelineMetricsSnapshot:
        """Return an immutable pipeline metrics snapshot."""
        return PipelineMetricsSnapshot(
            pipeline_id=self._pipeline_id,
            run_count=self._run_count,
            success_count=self._success_count,
            failure_count=self._failure_count,
            stage_success_counts=dict(self._stage_success_counts),
            stage_failure_counts=dict(self._stage_failure_counts),
            stage_records=tuple(self._stage_records),
            total_stage_duration_ms=self._total_stage_duration_ms,
            started_at=self._started_at,
            completed_at=self._completed_at,
            duration_ms=self._duration_ms,
        )

    def reset(self) -> None:
        """Clear collected pipeline metrics."""
        self._run_count = 0
        self._success_count = 0
        self._failure_count = 0
        self._stage_success_counts.clear()
        self._stage_failure_counts.clear()
        self._stage_records.clear()
        self._total_stage_duration_ms = 0.0
        self._started_at = None
        self._completed_at = None
        self._duration_ms = None
        self._stopwatch = Stopwatch()
        self._stage_watches.clear()
