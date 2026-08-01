"""Result metrics infrastructure."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class ResultMetricsSnapshot:
    """Immutable snapshot of result production counters.

    Counts and identifiers only. No interpretive summary text.
    """

    analysis_result_count: int
    final_result_count: int
    module_result_count: int
    stage_result_count: int
    success_count: int
    failure_count: int
    module_counts: Mapping[str, int] = field(default_factory=dict)
    stage_counts: Mapping[str, int] = field(default_factory=dict)
    score_count: int = 0
    decision_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible dictionary representation."""
        return {
            "analysis_result_count": self.analysis_result_count,
            "final_result_count": self.final_result_count,
            "module_result_count": self.module_result_count,
            "stage_result_count": self.stage_result_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "module_counts": dict(self.module_counts),
            "stage_counts": dict(self.stage_counts),
            "score_count": self.score_count,
            "decision_count": self.decision_count,
        }


class ResultMetrics:
    """Collect counters for produced analysis results.

    Infrastructure only. No interpretation and no report generation.
    """

    def __init__(self) -> None:
        """Initialize empty result metrics."""
        self._analysis_result_count = 0
        self._final_result_count = 0
        self._module_result_count = 0
        self._stage_result_count = 0
        self._success_count = 0
        self._failure_count = 0
        self._module_counts: dict[str, int] = {}
        self._stage_counts: dict[str, int] = {}
        self._score_count = 0
        self._decision_count = 0

    def record_analysis_result(self, *, success: bool, score_count: int = 0, decision_count: int = 0) -> None:
        """Record an analysis result publication."""
        self._analysis_result_count += 1
        self._score_count += score_count
        self._decision_count += decision_count
        self._record_success(success)

    def record_final_result(self, *, success: bool) -> None:
        """Record a final result publication."""
        self._final_result_count += 1
        self._record_success(success)

    def record_module_result(self, module_id: str, *, success: bool) -> None:
        """Record a module result publication."""
        self._module_result_count += 1
        self._module_counts[module_id] = self._module_counts.get(module_id, 0) + 1
        self._record_success(success)

    def record_stage_result(self, stage_id: str, *, success: bool) -> None:
        """Record a stage result publication."""
        self._stage_result_count += 1
        self._stage_counts[stage_id] = self._stage_counts.get(stage_id, 0) + 1
        self._record_success(success)

    def snapshot(self) -> ResultMetricsSnapshot:
        """Return an immutable result metrics snapshot."""
        return ResultMetricsSnapshot(
            analysis_result_count=self._analysis_result_count,
            final_result_count=self._final_result_count,
            module_result_count=self._module_result_count,
            stage_result_count=self._stage_result_count,
            success_count=self._success_count,
            failure_count=self._failure_count,
            module_counts=dict(self._module_counts),
            stage_counts=dict(self._stage_counts),
            score_count=self._score_count,
            decision_count=self._decision_count,
        )

    def reset(self) -> None:
        """Clear all result metrics counters."""
        self._analysis_result_count = 0
        self._final_result_count = 0
        self._module_result_count = 0
        self._stage_result_count = 0
        self._success_count = 0
        self._failure_count = 0
        self._module_counts.clear()
        self._stage_counts.clear()
        self._score_count = 0
        self._decision_count = 0

    def _record_success(self, success: bool) -> None:
        """Update success/failure counters."""
        if success:
            self._success_count += 1
        else:
            self._failure_count += 1
