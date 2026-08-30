"""Interpretation Builder tests (N-IMP-07)."""

from __future__ import annotations

from typing import Any

import pytest

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import CommercialRewriteContext, RewriteEngine
from engines.narrative_v2.interpretation import (
    FORMULA_STAGES,
    InterpretationBuilder,
    InterpretationError,
    InterpretationNarrative,
)


def _rewrite(case_0001_canonical: dict[str, Any]) -> CommercialRewriteContext:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    return RewriteEngine().rewrite(knowledge, reasoning, evidence)


def test_i1_accepts_rewrite_context_only(case_0001_canonical: dict[str, Any]) -> None:
    rewrite = _rewrite(case_0001_canonical)
    narrative = InterpretationBuilder().build(rewrite)
    assert isinstance(narrative, InterpretationNarrative)
    with pytest.raises(InterpretationError, match="CommercialRewriteContext only"):
        InterpretationBuilder().build(case_0001_canonical)


def test_i2_returns_interpretation_narrative(case_0001_canonical: dict[str, Any]) -> None:
    narrative = InterpretationBuilder().build(_rewrite(case_0001_canonical))
    assert isinstance(narrative, InterpretationNarrative)
    assert narrative.status in {"complete", "partial", "insufficient", "invalid"}


def test_i10_meaning_preserved(case_0001_canonical: dict[str, Any]) -> None:
    rewrite = _rewrite(case_0001_canonical)
    narrative = InterpretationBuilder().build(rewrite)
    meta = dict(narrative.metadata)
    primary = rewrite.item(meta["primary_rewrite_id"])
    assert primary is not None
    assert narrative.meaning is not None
    assert narrative.meaning == primary.customer_language
    assert primary.source_meaning.strip()


def test_i11_traceability(case_0001_canonical: dict[str, Any]) -> None:
    rewrite = _rewrite(case_0001_canonical)
    narrative = InterpretationBuilder().build(rewrite)
    rewrite_ids = {item.rewrite_id for item in rewrite.items}
    for ref in narrative.references:
        assert ref.rewrite_ids
        assert set(ref.rewrite_ids) <= rewrite_ids
        assert ref.knowledge_ids
        assert ref.reasoning_ids
        assert ref.evidence_ids


def test_i12_deterministic(case_0001_canonical: dict[str, Any]) -> None:
    rewrite = _rewrite(case_0001_canonical)
    first = InterpretationBuilder().build(rewrite)
    second = InterpretationBuilder().build(rewrite)
    assert first == second


def test_formula_metadata_recorded(case_0001_canonical: dict[str, Any]) -> None:
    narrative = InterpretationBuilder().build(_rewrite(case_0001_canonical))
    assert dict(narrative.metadata)["formula_stages"] == ",".join(FORMULA_STAGES)


def test_insufficient_when_no_core_insight() -> None:
    empty = CommercialRewriteContext(
        items=(),
        unresolved=(),
        references=(),
        metadata=(),
        status="insufficient",
    )
    narrative = InterpretationBuilder().build(empty)
    assert narrative.status == "insufficient"
    assert narrative.observation is None
    assert narrative.meaning is None
