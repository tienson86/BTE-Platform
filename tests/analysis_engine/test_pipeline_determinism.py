"""AX-2 deterministic repeated execution tests."""

from __future__ import annotations

from datetime import datetime, timezone

from engines.analysis_engine.pipeline.canonical_pipeline import CanonicalPipeline
from engines.analysis_engine.pipeline.stage_registry import ACTIVE_CANONICAL_STAGES

CHART = {
    "datetime": "1988-02-10T06:30:00",
    "timezone": "Asia/Ho_Chi_Minh",
    "month_branch": "yin",
    "day_master": "yi",
    "day_master_element": "wood",
    "season": "spring",
    "strength_level": "weak",
    "climate_type": "cold",
    "season_score": 44,
    "strength_score": 32,
    "temperature_score": 28,
    "pattern_score": 41,
    "pattern_quality": "average",
    "pattern_confidence": "medium",
    "pattern_integrity": 48,
    "pattern_stability": 45,
}


def _strip_times(payload: dict) -> dict:
    clone = dict(payload)
    trace = dict(clone.get("execution_trace") or {})
    trace["started_at"] = None
    trace["completed_at"] = None
    stages = []
    for entry in trace.get("stages") or []:
        item = dict(entry)
        item["started_at"] = None
        item["completed_at"] = None
        stages.append(item)
    trace["stages"] = stages
    clone["execution_trace"] = trace
    clone["diagnostics"] = [
        {key: value for key, value in item.items() if key != "details"}
        if isinstance(item, dict)
        else item
        for item in clone.get("diagnostics") or []
    ]
    return clone


def test_repeated_execution_is_deterministic() -> None:
    """Two fresh runs with the same chart must publish identical bindings."""
    first = CanonicalPipeline().run(CHART)
    second = CanonicalPipeline().run(CHART)
    assert first.success is True
    assert second.success is True
    assert first.stage_order == second.stage_order == ACTIVE_CANONICAL_STAGES
    assert first.seasonal == second.seasonal
    assert first.strength == second.strength
    assert first.temperature == second.temperature
    assert first.pattern == second.pattern
    assert first.pattern_evaluation == second.pattern_evaluation
    assert first.useful_god == second.useful_god
    assert first.package_versions == second.package_versions
    assert _strip_times(first.to_dict()) == _strip_times(second.to_dict())


def test_frozen_clock_makes_full_trace_identical() -> None:
    """A frozen clock yields byte-comparable execution traces."""
    frozen = datetime(2026, 8, 9, 12, 0, tzinfo=timezone.utc)

    def clock() -> datetime:
        return frozen

    first = CanonicalPipeline(clock=clock).run(CHART)
    second = CanonicalPipeline(clock=clock).run(CHART)
    assert first.execution_trace.to_dict() == second.execution_trace.to_dict()
    assert first.to_dict() == second.to_dict()
