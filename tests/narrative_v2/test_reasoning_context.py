"""NarrativeReasoningContext structure tests (N-IMP-03)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.reasoning import (
    ALLOWED_RELATION_TYPES,
    NarrativeReasoningContext,
    ReasoningBuilder,
)
from engines.narrative_v2.reasoning.reasoning_edge import (
    RELATION_QUALIFIES,
    RELATION_SUPPORTS,
)


FORBIDDEN_FIELDS: tuple[str, ...] = (
    "customer_text",
    "headline",
    "summary",
    "recommendation",
    "action",
    "warning",
)


def test_context_has_required_graph_fields(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    context = ReasoningBuilder().build(evidence)
    assert isinstance(context, NarrativeReasoningContext)
    assert context.nodes
    assert context.edges
    assert context.observations
    assert context.boundaries or context.status == "active"
    assert context.references
    assert context.metadata
    assert context.status in {"active", "insufficient"}
    meta = dict(context.metadata)
    assert meta["shadow_mode"] == "true"
    assert "headline" not in meta
    assert "summary" not in meta


def test_context_does_not_include_customer_fields(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    context = ReasoningBuilder().build(evidence)
    for field in FORBIDDEN_FIELDS:
        assert not hasattr(context, field)
    assert not hasattr(context, "canonical_analysis")


def test_qualification_edges_are_preserved(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    context = ReasoningBuilder().build(evidence)
    ten_gods_edges = [
        edge
        for edge in context.edges
        if "pattern_ten_gods_relation" in edge.edge_id
    ]
    types = {edge.relation_type for edge in ten_gods_edges}
    assert RELATION_QUALIFIES in types
    assert RELATION_SUPPORTS in types
    for edge in ten_gods_edges:
        assert edge.relation_type in ALLOWED_RELATION_TYPES
