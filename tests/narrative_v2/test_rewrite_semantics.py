"""Semantic preservation and negative tests for rewrite (N-IMP-05)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine


def test_rw6_rw7_rw8_no_escalation_prediction_or_action(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    context = RewriteEngine().rewrite(knowledge)
    blob = " ".join(item.customer_language for item in context.items)
    assert "chắc chắn" not in blob
    assert "sẽ ly hôn" not in blob
    assert "tình duyên chắc chắn" not in blob
    assert "màu đỏ" not in blob
    assert "hướng Nam" not in blob
    assert "Bạn nên dùng màu đỏ" not in blob


def test_rw9_no_raw_technical_leak(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    context = RewriteEngine().rewrite(knowledge)
    blob = " ".join(item.customer_language for item in context.items)
    assert "Engine" not in blob
    assert "NR-REL" not in blob
    assert "{{" not in blob
    assert "CanonicalAnalysis" not in blob


def test_useful_god_does_not_become_fengshui_action(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    context = RewriteEngine().rewrite(knowledge)
    useful = [
        item
        for item in context.items
        if "useful_god" in item.source_knowledge_ids[0]
    ]
    blob = " ".join(item.customer_language for item in useful)
    assert "màu đỏ" not in blob
    assert "hướng Nam" not in blob
    assert "nghề Hỏa" not in blob


def test_shensha_does_not_become_prediction(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    context = RewriteEngine().rewrite(knowledge)
    shensha = [
        item for item in context.items if item.domain == "shensha"
    ]
    blob = " ".join(item.customer_language for item in shensha)
    assert "tình duyên chắc chắn" not in blob
    assert "luôn gặp may" not in blob
