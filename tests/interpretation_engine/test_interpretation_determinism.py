"""Deterministic Canonical Interpretation Pipeline execution tests."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from engines.interpretation_engine.pipeline.canonical_interpretation_pipeline import (
    CanonicalInterpretationPipeline,
)
from tests.interpretation_engine.ie1_snapshots import ax2_snapshot, ax3_snapshot, ax4_snapshot


def _clock() -> datetime:
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def test_two_runs_are_byte_identical() -> None:
    """Same inputs and clock yield identical published JSON."""
    analysis = ax2_snapshot()
    decision = ax3_snapshot()
    luck = ax4_snapshot()
    first = CanonicalInterpretationPipeline(clock=_clock).run(
        analysis_result=analysis,
        decision_result=decision,
        luck_result=luck,
    )
    second = CanonicalInterpretationPipeline(clock=_clock).run(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
    )
    encoded_first = json.dumps(first.to_dict(), sort_keys=True, ensure_ascii=False)
    encoded_second = json.dumps(second.to_dict(), sort_keys=True, ensure_ascii=False)
    assert encoded_first == encoded_second
    assert first.interpretation_trace.started_at == "2026-08-09T12:00:00Z"
    assert first.knowledge_result["candidates"] == second.knowledge_result["candidates"]
    assert first.composition_result["sections"] == second.composition_result["sections"]
