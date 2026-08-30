"""KnowledgeValidator tests (N-IMP-04)."""

from __future__ import annotations

from typing import Any

import pytest

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import (
    KnowledgeItem,
    KnowledgeReference,
    KnowledgeResolver,
    KnowledgeValidationError,
    KnowledgeValidator,
    NarrativeKnowledgeContext,
)
from engines.narrative_v2.reasoning import ReasoningBuilder


def _built(case_0001_canonical: dict[str, Any]) -> tuple[object, object, object]:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    return knowledge, reasoning, evidence


def test_case_0001_passes_validator(case_0001_canonical: dict[str, Any]) -> None:
    knowledge, reasoning, evidence = _built(case_0001_canonical)
    outcome = KnowledgeValidator().validate(knowledge, reasoning, evidence)
    assert outcome.passed is True
    assert outcome.status == "PASS"


def test_k19_raw_debug_rejected(case_0001_canonical: dict[str, Any]) -> None:
    knowledge, reasoning, evidence = _built(case_0001_canonical)
    item = knowledge.items[0]
    broken = KnowledgeItem(
        knowledge_id=item.knowledge_id,
        domain=item.domain,
        semantic_key=item.semantic_key,
        knowledge_type=item.knowledge_type,
        status=item.status,
        technical_meaning={"debug": True},  # type: ignore[arg-type]
        customer_meaning_candidate=item.customer_meaning_candidate,
        boundaries=item.boundaries,
        recommendations=item.recommendations,
        references=item.references,
        source_path=item.source_path,
        version=item.version,
    )
    context = NarrativeKnowledgeContext(
        items=(broken,),
        matches=knowledge.matches,
        unresolved=knowledge.unresolved,
        references=knowledge.references,
        metadata=knowledge.metadata,
        status=knowledge.status,
        contract_gaps=knowledge.contract_gaps,
    )
    with pytest.raises(KnowledgeValidationError, match="debug"):
        KnowledgeValidator().assert_valid(context, reasoning, evidence)


def test_k20_unapproved_status_rejected(case_0001_canonical: dict[str, Any]) -> None:
    knowledge, reasoning, evidence = _built(case_0001_canonical)
    item = knowledge.items[0]
    broken = KnowledgeItem(
        knowledge_id=item.knowledge_id,
        domain=item.domain,
        semantic_key=item.semantic_key,
        knowledge_type=item.knowledge_type,
        status="draft",
        technical_meaning=item.technical_meaning,
        customer_meaning_candidate=item.customer_meaning_candidate,
        boundaries=item.boundaries,
        recommendations=item.recommendations,
        references=item.references,
        source_path=item.source_path,
        version=item.version,
    )
    context = NarrativeKnowledgeContext(
        items=(broken,),
        matches=(),
        unresolved=(),
        references=(
            KnowledgeReference(
                source_path=item.source_path,
                knowledge_id=item.knowledge_id,
                version=item.version,
                status="draft",
                reasoning_ids=item.references[0].reasoning_ids,
                evidence_ids=item.references[0].evidence_ids,
            ),
        ),
        metadata=knowledge.metadata,
        status=knowledge.status,
    )
    with pytest.raises(KnowledgeValidationError, match="not approved"):
        KnowledgeValidator().assert_valid(context, reasoning, evidence)
