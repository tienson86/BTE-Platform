"""Interpretation Formula tests (N-IMP-07)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine
from engines.narrative_v2.interpretation import FORMULA_STAGES, InterpretationBuilder
from engines.narrative_v2.interpretation.interpretation_formula import (
    CORE_SEMANTIC_PRIORITY,
    join_sentences,
    split_sentences,
)


def test_i3_formula_stage_order() -> None:
    assert FORMULA_STAGES == (
        "observation",
        "reasoning",
        "meaning",
        "impact",
        "recommendation",
        "closing",
    )
    assert CORE_SEMANTIC_PRIORITY[0] == "core.pattern_context"


def test_i3_case_0001_visits_every_formula_stage(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    narrative = InterpretationBuilder().build(rewrite)
    for stage in FORMULA_STAGES:
        value = getattr(narrative, stage)
        assert isinstance(value, str) and value.strip()
    assert narrative.overview
    assert narrative.observation != narrative.meaning
    assert narrative.overview != narrative.closing


def test_split_join_preserves_rewrite_units() -> None:
    text = "Bạn có chỗ dưỡng, chịu được việc cần nền. Hữu ích khi cần ủ và học có khung."
    parts = split_sentences(text)
    assert len(parts) == 2
    assert join_sentences(parts) == text
