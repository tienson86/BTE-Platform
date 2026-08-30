"""RewriteValidator tests (N-IMP-05)."""

from __future__ import annotations

from typing import Any

import pytest

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import (
    RewriteEngine,
    RewriteItem,
    RewriteValidationError,
    RewriteValidator,
    CommercialRewriteContext,
)


def _built(case_0001_canonical: dict[str, Any]) -> tuple[object, object]:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge)
    return rewrite, knowledge


def test_case_0001_passes_validator(case_0001_canonical: dict[str, Any]) -> None:
    rewrite, knowledge = _built(case_0001_canonical)
    outcome = RewriteValidator().validate(rewrite, knowledge)
    assert outcome.passed is True
    assert outcome.status == "PASS"


def test_escalation_is_rejected(case_0001_canonical: dict[str, Any]) -> None:
    rewrite, knowledge = _built(case_0001_canonical)
    if not rewrite.items:
        pytest.skip("no rewritten units")
    item = rewrite.items[0]
    broken = RewriteItem(
        rewrite_id=item.rewrite_id,
        semantic_key=item.semantic_key,
        domain=item.domain,
        source_knowledge_ids=item.source_knowledge_ids,
        source_reasoning_ids=item.source_reasoning_ids,
        source_evidence_ids=item.source_evidence_ids,
        source_meaning=item.source_meaning,
        normalized_meaning="Bạn chắc chắn thành công.",
        customer_language="Bạn chắc chắn thành công.",
        strategy=item.strategy,
        style=item.style,
        status=item.status,
        references=item.references,
    )
    context = CommercialRewriteContext(
        items=(broken,),
        unresolved=(),
        references=rewrite.references,
        metadata=rewrite.metadata,
        status=rewrite.status,
        contract_gaps=rewrite.contract_gaps,
    )
    with pytest.raises(RewriteValidationError):
        RewriteValidator().assert_valid(context, knowledge)
