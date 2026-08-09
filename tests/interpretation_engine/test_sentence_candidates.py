"""IE-2 sentence candidate builder tests."""

from __future__ import annotations

import json

from engines.interpretation_engine.context.canonical_interpretation_context import (
    build_interpretation_context,
)
from engines.interpretation_engine.knowledge.composition_context import build_composition_context
from engines.interpretation_engine.knowledge.sentence_candidate_builder import (
    SentenceCandidateBuilder,
)
from tests.interpretation_engine.ie1_snapshots import ax2_snapshot, ax3_snapshot, ax4_snapshot


def _run():
    interpretation = build_interpretation_context(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
    )
    context = build_composition_context(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
        interpretation_context=interpretation,
    )
    return SentenceCandidateBuilder().run(context)


def test_candidates_are_structured_not_paragraphs() -> None:
    """Candidates expose required ids and values without composed prose."""
    result = _run()
    assert result.success is True
    assert result.ai_rewrite["enabled"] is False
    assert result.candidates
    required = {
        "sentence_id",
        "template_id",
        "placeholder_values",
        "evidence_ids",
        "reasoning_ids",
        "confidence",
        "references",
    }
    for candidate in result.candidates:
        payload = candidate.to_dict()
        assert required.issubset(payload)
        assert payload["sentence_id"].startswith("SC-")
        assert "narrative" not in payload
        assert isinstance(payload["placeholder_values"], dict)


def test_repeated_runs_are_deterministic() -> None:
    """Same snapshots yield identical candidate JSON."""
    first = json.dumps(_run().to_dict(), sort_keys=True, ensure_ascii=False)
    second = json.dumps(_run().to_dict(), sort_keys=True, ensure_ascii=False)
    assert first == second
