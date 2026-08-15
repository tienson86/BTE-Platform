"""Recommendation Composer — from knowledge/decision/state/relationship, never score."""

from __future__ import annotations

from engines.interpretation_engine.foundation.narrative.constants import (
    KIND_RECOMMENDATION,
    KIND_WARNING,
    SCORE_FIELD_NAMES,
)
from engines.interpretation_engine.foundation.narrative.dedup import (
    merge_recommendations,
    merge_warnings,
)
from engines.interpretation_engine.foundation.narrative.models import (
    EvidenceGraph,
    EvidenceNode,
    RecommendationItem,
    WarningItem,
)


def compose_recommendations(
    graph: EvidenceGraph,
) -> tuple[RecommendationItem, ...]:
    """Copy recommendations that already reference evidence. Never use score."""
    items: list[RecommendationItem] = []
    for index, node in enumerate(graph.nodes):
        if node.kind != KIND_RECOMMENDATION:
            continue
        if _looks_like_score(node):
            continue
        items.append(
            RecommendationItem(
                recommendation_id=f"rec:{node.bundle_id}:{index}",
                action=node.statement,
                rationale=node.rationale,
                category=node.category,
                evidence_ids=(node.evidence_id, *node.alias_ids),
                bundle_id=node.bundle_id,
                domain=node.domain,
                customer_domain=node.customer_domain,
                confidence=node.confidence,
                importance=node.importance,
            )
        )
    return merge_recommendations(tuple(items))


def compose_warnings(graph: EvidenceGraph) -> tuple[WarningItem, ...]:
    """Copy warnings that already reference evidence. Never use score."""
    items: list[WarningItem] = []
    for index, node in enumerate(graph.nodes):
        if node.kind != KIND_WARNING:
            continue
        if _looks_like_score(node):
            continue
        items.append(
            WarningItem(
                warning_id=f"warn:{node.bundle_id}:{index}",
                risk=node.statement,
                condition=node.condition,
                mitigation=node.mitigation,
                evidence_ids=(node.evidence_id, *node.alias_ids),
                bundle_id=node.bundle_id,
                domain=node.domain,
                confidence=node.confidence,
                importance=node.importance,
            )
        )
    return merge_warnings(tuple(items))


def _looks_like_score(node: EvidenceNode) -> bool:
    """Reject score-derived statements. Recommendations never come from score."""
    ref = node.engine_truth_ref.casefold()
    return any(name in ref.split(":") for name in SCORE_FIELD_NAMES)
