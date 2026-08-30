"""Language Standard tests for Commercial Rewrite (N-IMP-05)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine
from engines.narrative_v2.rewrite.rewrite_strategy import CUSTOMER_ADDRESS


def test_rw14_rw15_customer_address_and_language_standard(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    context = RewriteEngine().rewrite(knowledge)
    assert context.items
    for item in context.items:
        assert CUSTOMER_ADDRESS in item.customer_language
        assert "đương số" not in item.customer_language.casefold()
        assert "mệnh chủ" not in item.customer_language.casefold()
        assert "chắc chắn" not in item.customer_language
        assert "đại cát" not in item.customer_language


def test_rw16_terminology_is_metadata_not_requirement(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    context = RewriteEngine().rewrite(knowledge)
    for item in context.items:
        meta = dict(item.metadata)
        assert "terminology" in meta
        assert item.customer_language != meta["terminology"]
        assert "Dụng thần" not in item.customer_language
