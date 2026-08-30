"""Determinism tests for Commercial Rewrite (N-IMP-05)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine


def test_rw12_no_random_variant_selection(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    first = RewriteEngine().rewrite(knowledge)
    second = RewriteEngine().rewrite(knowledge)
    assert first.items == second.items
    assert first.unresolved == second.unresolved
    for item in first.items:
        assert item.strategy in {
            "clarification",
            "professionalization",
            "simplification",
            "contextualization",
            "action_orientation",
        }
