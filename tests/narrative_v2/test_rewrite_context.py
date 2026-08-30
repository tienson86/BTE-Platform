"""CommercialRewriteContext structure tests (N-IMP-05)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import CommercialRewriteContext, RewriteEngine

FORBIDDEN_FIELDS: tuple[str, ...] = (
    "overview",
    "interpretation",
    "action_plan",
    "presentation",
    "final_summary",
)


def test_context_has_required_fields(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    context = RewriteEngine().rewrite(knowledge)
    assert isinstance(context, CommercialRewriteContext)
    assert context.unresolved
    assert context.metadata
    assert context.status in {"rewritten", "partial", "unresolved"}
    meta = dict(context.metadata)
    assert meta["shadow_mode"] == "true"
    assert meta["sentence_library"] in {"approved", "partial"}


def test_context_does_not_include_final_narrative_fields(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    context = RewriteEngine().rewrite(knowledge)
    for field in FORBIDDEN_FIELDS:
        assert not hasattr(context, field)
    assert not hasattr(context, "canonical_analysis")
