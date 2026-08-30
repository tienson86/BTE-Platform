"""Decision Builder tests (N-IMP-08)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.action import DecisionBuilder
from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.interpretation import InterpretationBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine


def _pair(case_0001_canonical: dict[str, Any]) -> tuple[object, object]:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    interpretation = InterpretationBuilder().build(rewrite)
    return rewrite, interpretation


def test_a6_decision_traces_to_knowledge(case_0001_canonical: dict[str, Any]) -> None:
    rewrite, interpretation = _pair(case_0001_canonical)
    context = DecisionBuilder().build(rewrite, interpretation)
    assert context.items
    for decision in context.items:
        assert decision.source_knowledge_ids
        assert decision.source_rewrite_ids
        assert decision.source_reasoning_ids
        assert decision.source_evidence_ids
        known = {kid for item in rewrite.items for kid in item.source_knowledge_ids}
        assert set(decision.source_knowledge_ids) <= known


def test_decision_is_deterministic(case_0001_canonical: dict[str, Any]) -> None:
    rewrite, interpretation = _pair(case_0001_canonical)
    first = DecisionBuilder().build(rewrite, interpretation)
    second = DecisionBuilder().build(rewrite, interpretation)
    assert first == second
    ids = [item.decision_id for item in first.items]
    assert ids == [item.decision_id for item in sorted(first.items, key=lambda item: (-item.priority, item.decision_id))]
