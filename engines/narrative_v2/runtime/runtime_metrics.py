"""Narrative V2 runtime metrics.

Collects duration and counts. No dashboard.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RuntimeMetrics:
    """Skeleton runtime metrics."""

    runtime_duration: float = 0.0
    stage_duration: dict[str, float] = field(default_factory=dict)
    builder_count: int = 0
    error_count: int = 0

    def record_stage(self, stage: str, duration: float) -> None:
        """Record duration for one stage."""
        self.stage_duration[stage] = duration
