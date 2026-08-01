"""Rule metrics infrastructure."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class RuleMetricsSnapshot:
    """Immutable snapshot of rule access/evaluation counters.

    Counts only. Does not store rule content or evaluation logic.
    """

    lookup_count: int
    evaluation_count: int
    match_count: int
    miss_count: int
    error_count: int
    rule_lookup_counts: Mapping[str, int] = field(default_factory=dict)
    rule_match_counts: Mapping[str, int] = field(default_factory=dict)
    rule_miss_counts: Mapping[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible dictionary representation."""
        return {
            "lookup_count": self.lookup_count,
            "evaluation_count": self.evaluation_count,
            "match_count": self.match_count,
            "miss_count": self.miss_count,
            "error_count": self.error_count,
            "rule_lookup_counts": dict(self.rule_lookup_counts),
            "rule_match_counts": dict(self.rule_match_counts),
            "rule_miss_counts": dict(self.rule_miss_counts),
        }


class RuleMetrics:
    """Collect rule lookup/evaluation counters without executing rules.

    Infrastructure only. No rule interpretation and no dashboards.
    """

    def __init__(self) -> None:
        """Initialize empty rule metrics."""
        self._lookup_count = 0
        self._evaluation_count = 0
        self._match_count = 0
        self._miss_count = 0
        self._error_count = 0
        self._rule_lookup_counts: dict[str, int] = {}
        self._rule_match_counts: dict[str, int] = {}
        self._rule_miss_counts: dict[str, int] = {}

    def record_lookup(self, rule_id: str) -> None:
        """Record a rule lookup by identifier."""
        self._lookup_count += 1
        self._rule_lookup_counts[rule_id] = self._rule_lookup_counts.get(rule_id, 0) + 1

    def record_evaluation(self, rule_id: str, *, matched: bool) -> None:
        """Record a rule evaluation outcome counter."""
        self._evaluation_count += 1
        if matched:
            self._match_count += 1
            self._rule_match_counts[rule_id] = self._rule_match_counts.get(rule_id, 0) + 1
        else:
            self._miss_count += 1
            self._rule_miss_counts[rule_id] = self._rule_miss_counts.get(rule_id, 0) + 1

    def record_miss(self, rule_id: str) -> None:
        """Record a rule miss without a full evaluation event."""
        self._miss_count += 1
        self._rule_miss_counts[rule_id] = self._rule_miss_counts.get(rule_id, 0) + 1

    def record_error(self, rule_id: str | None = None) -> None:
        """Record a rule access/evaluation infrastructure error."""
        self._error_count += 1
        if rule_id is not None:
            # Track under lookup map for visibility without inventing semantics.
            self._rule_lookup_counts.setdefault(rule_id, 0)

    def snapshot(self) -> RuleMetricsSnapshot:
        """Return an immutable rule metrics snapshot."""
        return RuleMetricsSnapshot(
            lookup_count=self._lookup_count,
            evaluation_count=self._evaluation_count,
            match_count=self._match_count,
            miss_count=self._miss_count,
            error_count=self._error_count,
            rule_lookup_counts=dict(self._rule_lookup_counts),
            rule_match_counts=dict(self._rule_match_counts),
            rule_miss_counts=dict(self._rule_miss_counts),
        )

    def reset(self) -> None:
        """Clear all rule metrics counters."""
        self._lookup_count = 0
        self._evaluation_count = 0
        self._match_count = 0
        self._miss_count = 0
        self._error_count = 0
        self._rule_lookup_counts.clear()
        self._rule_match_counts.clear()
        self._rule_miss_counts.clear()
