"""Shared IE-3 test helpers. Reuses IE-1 snapshots and IE-2 selection."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from engines.interpretation_engine.context.canonical_interpretation_context import (
    build_interpretation_context,
)
from engines.interpretation_engine.knowledge.composition_context import build_composition_context
from engines.interpretation_engine.knowledge.sentence_candidate_builder import (
    SentenceCandidateBuilder,
)
from tests.interpretation_engine.ie1_snapshots import ax2_snapshot, ax3_snapshot, ax4_snapshot


def frozen_clock() -> datetime:
    """Return a fixed UTC clock for deterministic traces."""
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def assemble_inputs() -> dict[str, Any]:
    """Build sealed IE-1 context plus IE-2 composition result."""
    analysis = ax2_snapshot()
    decision = ax3_snapshot()
    luck = ax4_snapshot()
    interpretation = build_interpretation_context(
        analysis_result=analysis,
        decision_result=decision,
        luck_result=luck,
    )
    selection_context = build_composition_context(
        analysis_result=analysis,
        decision_result=decision,
        luck_result=luck,
        interpretation_context=interpretation,
    )
    selection = SentenceCandidateBuilder().run(selection_context)
    return {
        "analysis_result": analysis,
        "decision_result": decision,
        "luck_result": luck,
        "interpretation_context": interpretation,
        "composition_result": selection,
    }
