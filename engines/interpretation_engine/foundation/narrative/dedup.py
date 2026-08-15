"""Deduplicate evidence, recommendations, and warnings before rendering."""

from __future__ import annotations

from engines.interpretation_engine.foundation.narrative.mapping import rank_key
from engines.interpretation_engine.foundation.narrative.models import (
    EvidenceGraph,
    EvidenceNode,
    RecommendationItem,
    WarningItem,
)
from engines.interpretation_engine.foundation.narrative.text import fingerprint


def merge_evidence_nodes(nodes: tuple[EvidenceNode, ...]) -> EvidenceGraph:
    """Merge duplicated evidence statements. Keep the higher-ranked copy."""
    ranked = sorted(
        nodes,
        key=lambda item: rank_key(item.domain, item.importance, item.confidence),
        reverse=True,
    )
    chosen: dict[tuple[str, str], EvidenceNode] = {}
    aliases: dict[tuple[str, str], list[str]] = {}
    for node in ranked:
        key = (node.kind, fingerprint(node.statement))
        if not key[1]:
            continue
        if key not in chosen:
            chosen[key] = node
            aliases[key] = []
            continue
        aliases[key].append(node.evidence_id)
    merged = tuple(
        _with_aliases(node, tuple(aliases[(node.kind, fingerprint(node.statement))]))
        for node in chosen.values()
    )
    return EvidenceGraph(
        nodes=merged,
        raw_count=len(nodes),
        merged_count=len(merged),
    )


def merge_recommendations(
    items: tuple[RecommendationItem, ...],
) -> tuple[RecommendationItem, ...]:
    """Merge duplicated recommendation actions and union evidence ids."""
    ranked = sorted(
        items,
        key=lambda item: rank_key(item.domain, item.importance, item.confidence),
        reverse=True,
    )
    chosen: dict[str, RecommendationItem] = {}
    for item in ranked:
        key = fingerprint(item.action)
        if not key:
            continue
        existing = chosen.get(key)
        if existing is None:
            chosen[key] = item
            continue
        chosen[key] = RecommendationItem(
            recommendation_id=existing.recommendation_id,
            action=existing.action,
            rationale=existing.rationale or item.rationale,
            category=existing.category or item.category,
            evidence_ids=tuple(dict.fromkeys([*existing.evidence_ids, *item.evidence_ids])),
            bundle_id=existing.bundle_id,
            domain=existing.domain,
            customer_domain=existing.customer_domain or item.customer_domain,
            confidence=existing.confidence,
            importance=existing.importance,
        )
    return tuple(chosen.values())


def merge_warnings(items: tuple[WarningItem, ...]) -> tuple[WarningItem, ...]:
    """Merge duplicated warning risks and union evidence ids."""
    ranked = sorted(
        items,
        key=lambda item: rank_key(item.domain, item.importance, item.confidence),
        reverse=True,
    )
    chosen: dict[str, WarningItem] = {}
    for item in ranked:
        key = fingerprint(item.risk)
        if not key:
            continue
        existing = chosen.get(key)
        if existing is None:
            chosen[key] = item
            continue
        chosen[key] = WarningItem(
            warning_id=existing.warning_id,
            risk=existing.risk,
            condition=existing.condition or item.condition,
            mitigation=existing.mitigation or item.mitigation,
            evidence_ids=tuple(dict.fromkeys([*existing.evidence_ids, *item.evidence_ids])),
            bundle_id=existing.bundle_id,
            domain=existing.domain,
            confidence=existing.confidence,
            importance=existing.importance,
        )
    return tuple(chosen.values())


def _with_aliases(node: EvidenceNode, alias_ids: tuple[str, ...]) -> EvidenceNode:
    """Attach merged alias ids onto the surviving evidence node."""
    if not alias_ids:
        return node
    return EvidenceNode(
        evidence_id=node.evidence_id,
        bundle_id=node.bundle_id,
        bundle_kind=node.bundle_kind,
        domain=node.domain,
        kind=node.kind,
        slot=node.slot,
        statement=node.statement,
        engine_truth_ref=node.engine_truth_ref,
        customer_domain=node.customer_domain,
        category=node.category,
        rationale=node.rationale,
        condition=node.condition,
        mitigation=node.mitigation,
        confidence=node.confidence,
        importance=node.importance,
        alias_ids=alias_ids,
    )
