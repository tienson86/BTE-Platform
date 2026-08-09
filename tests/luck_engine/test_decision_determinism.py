"""Deterministic Luck Decision execution tests."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from engines.luck_engine.analysis import LuckAnalysisEngine
from engines.luck_engine.decision import LuckDecisionEngine
from engines.luck_engine.timeline import construct_timeline


def _clock() -> datetime:
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def test_two_runs_are_byte_identical(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Same inputs and clock yield identical published JSON."""
    timeline = construct_timeline(**continuous_timeline_payload)
    luck_analysis = LuckAnalysisEngine(clock=_clock).run(
        timeline=timeline,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    engine = LuckDecisionEngine(clock=_clock)
    first = engine.run(
        timeline_result=timeline,
        luck_analysis_result=luck_analysis,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    second = engine.run(
        timeline_result=timeline,
        luck_analysis_result=luck_analysis,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    encoded_first = json.dumps(first.to_dict(), sort_keys=True, ensure_ascii=False)
    encoded_second = json.dumps(second.to_dict(), sort_keys=True, ensure_ascii=False)
    assert encoded_first == encoded_second
    assert first.opportunity_score["value"] == second.opportunity_score["value"]
    assert first.decision_trace.started_at == "2026-08-09T12:00:00Z"
