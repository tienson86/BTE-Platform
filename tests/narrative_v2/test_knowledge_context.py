"""NarrativeKnowledgeContext structure tests (N-IMP-04)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver, NarrativeKnowledgeContext
from engines.narrative_v2.reasoning import ReasoningBuilder

FORBIDDEN_FIELDS: tuple[str, ...] = (
    "final_summary",
    "final_interpretation",
    "final_action_plan",
    "presentation",
    "action_plan",
)


def test_context_has_required_fields(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    context = KnowledgeResolver().resolve(reasoning, evidence)
    assert isinstance(context, NarrativeKnowledgeContext)
    assert context.items
    assert context.matches
    assert context.unresolved
    assert context.references
    assert context.metadata
    assert context.status in {"resolved", "unresolved", "partial"}
    meta = dict(context.metadata)
    assert meta["shadow_mode"] == "true"
    assert meta["resolver_version"]


def test_context_does_not_include_final_narrative_fields(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    context = KnowledgeResolver().resolve(reasoning, evidence)
    for field in FORBIDDEN_FIELDS:
        assert not hasattr(context, field)
    assert not hasattr(context, "canonical_analysis")
