"""AX-3 deterministic Decision Pipeline tests."""

from __future__ import annotations

from datetime import datetime, timezone

from engines.decision_engine.pipeline.canonical_decision_pipeline import (
    CanonicalDecisionPipeline,
)
from engines.decision_engine.pipeline.stage_registry import ACTIVE_DECISION_STAGES

SNAPSHOT = {
    "datetime": "1988-02-10T06:30:00",
    "season_score": 44,
    "strength_score": 32,
    "temperature_score": 28,
    "pattern_score": 41,
    "pattern_quality": "average",
    "pattern_confidence": "medium",
    "pattern_integrity": 48,
    "pattern_stability": 45,
    "useful_god": "Chính Ấn",
    "favorable_gods": ["Chính Ấn"],
    "unfavorable_gods": ["Thất Sát"],
    "decision_confidence": "medium",
    "decision_score": 41,
    "decision_reasoning": "Weak published decision.",
    "decision_diagnostics": [],
}


def _strip_times(payload: dict) -> dict:
    clone = dict(payload)
    trace = dict(clone.get("decision_trace") or {})
    trace["started_at"] = None
    trace["completed_at"] = None
    steps = []
    for entry in trace.get("steps") or []:
        item = dict(entry)
        item["timestamp"] = None
        steps.append(item)
    trace["steps"] = steps
    clone["decision_trace"] = trace
    return clone


def test_repeated_execution_is_deterministic() -> None:
    """Two fresh runs with the same snapshot must publish identical bindings."""
    first = CanonicalDecisionPipeline().run(SNAPSHOT)
    second = CanonicalDecisionPipeline().run(SNAPSHOT)
    assert first.success is True
    assert second.success is True
    assert first.stage_order == second.stage_order == ACTIVE_DECISION_STAGES
    assert first.foundation == second.foundation
    assert first.priority == second.priority
    assert first.override == second.override
    assert first.final_useful_god == second.final_useful_god
    assert first.package_versions == second.package_versions
    assert _strip_times(first.to_dict()) == _strip_times(second.to_dict())


def test_frozen_clock_makes_full_trace_identical() -> None:
    """A frozen clock yields byte-comparable decision traces."""
    frozen = datetime(2026, 8, 9, 12, 0, tzinfo=timezone.utc)

    def clock() -> datetime:
        return frozen

    first = CanonicalDecisionPipeline(clock=clock).run(SNAPSHOT)
    second = CanonicalDecisionPipeline(clock=clock).run(SNAPSHOT)
    assert first.decision_trace is not None
    assert second.decision_trace is not None
    assert first.decision_trace.to_dict() == second.decision_trace.to_dict()
    assert first.to_dict() == second.to_dict()
