"""Deterministic Canonical Luck Pipeline execution tests."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from engines.luck_engine.pipeline.canonical_luck_pipeline import CanonicalLuckPipeline


def _clock() -> datetime:
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def test_two_runs_are_byte_identical(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Same inputs and clock yield identical published JSON."""
    pipeline = CanonicalLuckPipeline(clock=_clock)
    first = pipeline.run(
        timeline=continuous_timeline_payload,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    second = CanonicalLuckPipeline(clock=_clock).run(
        timeline=continuous_timeline_payload,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    encoded_first = json.dumps(first.to_dict(), sort_keys=True, ensure_ascii=False)
    encoded_second = json.dumps(second.to_dict(), sort_keys=True, ensure_ascii=False)
    assert encoded_first == encoded_second
    assert first.luck_trace.started_at == "2026-08-09T12:00:00Z"
    assert first.decision_result["opportunity_score"] == second.decision_result["opportunity_score"]
    assert first.decision_result["risk_score"] == second.decision_result["risk_score"]
