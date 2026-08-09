"""Deterministic Luck Analysis execution tests."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from engines.luck_engine.analysis.luck_analysis_engine import LuckAnalysisEngine
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
    engine = LuckAnalysisEngine(clock=_clock)
    first = engine.run(
        timeline=timeline,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    second = engine.run(
        timeline=timeline,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    encoded_first = json.dumps(first.to_dict(), sort_keys=True, ensure_ascii=False)
    encoded_second = json.dumps(second.to_dict(), sort_keys=True, ensure_ascii=False)
    assert encoded_first == encoded_second
    assert first.seasonal_impact["score"]["value"] == second.seasonal_impact["score"]["value"]
    assert first.analysis_trace.started_at == "2026-08-09T12:00:00Z"
