"""Knowledge approval-policy tests (N-IMP-04)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import KnowledgeLoader, KnowledgeResolver
from engines.narrative_v2.knowledge.knowledge_status import (
    ELIGIBLE_SOURCE_STATUSES,
    STATUS_APPROVED,
)
from engines.narrative_v2.reasoning import ReasoningBuilder


def test_k4_k5_k20_approval_status_enforced() -> None:
    assert ELIGIBLE_SOURCE_STATUSES == frozenset({STATUS_APPROVED})
    for record in KnowledgeLoader().load_index().records():
        assert record.status == STATUS_APPROVED
        assert record.customer_meaning_candidate is None


def test_k5_technical_only_not_used_as_customer_meaning(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    context = KnowledgeResolver().resolve(reasoning, evidence)
    for item in context.items:
        assert item.customer_meaning_candidate is None
        assert item.technical_meaning is None or isinstance(item.technical_meaning, str)


def test_shensha_resolves_without_romance_derivation(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    context = KnowledgeResolver().resolve(reasoning, evidence)
    hong = context.item("knowledge.shensha.hong_loan")
    assert hong is not None
    assert hong.status == STATUS_APPROVED
    assert hong.customer_meaning_candidate is None
    blob = " ".join(
        part
        for part in (hong.technical_meaning, *(hong.recommendations), *(hong.boundaries))
        if part
    )
    assert "Tình duyên thuận lợi" not in blob
    assert any(
        match.semantic_key == "boundary.approved_rule_unavailable"
        for match in context.matches
        if match.knowledge_id == "knowledge.shensha.hong_loan"
    )
