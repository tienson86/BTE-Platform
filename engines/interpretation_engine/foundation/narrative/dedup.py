"""Deduplicate by evidence identity, not identical wording."""

from __future__ import annotations

from engines.interpretation_engine.foundation.narrative.mapping import (
    customer_relevance,
    evidence_identity,
    rank_key,
)
from engines.interpretation_engine.foundation.narrative.models import (
    EvidenceGraph,
    EvidenceNode,
    RecommendationItem,
    WarningItem,
)
from engines.interpretation_engine.foundation.narrative.text import fingerprint


def merge_evidence_nodes(nodes: tuple[EvidenceNode, ...]) -> EvidenceGraph:
    """Merge nodes that share engine-truth evidence. Keep the higher-ranked copy."""
    ranked = sorted(nodes, key=_node_rank, reverse=True)
    chosen: dict[str, EvidenceNode] = {}
    aliases: dict[str, list[str]] = {}
    for node in ranked:
        key = evidence_identity(node.kind, node.engine_truth_ref, node.evidence_id)
        if not key:
            continue
        if key not in chosen:
            chosen[key] = node
            aliases[key] = []
            continue
        aliases[key].append(node.evidence_id)
    merged = tuple(
        _with_aliases(
            node,
            tuple(aliases[evidence_identity(node.kind, node.engine_truth_ref, node.evidence_id)]),
        )
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
    """Merge recommendations that share evidence, then drop repeated actions."""
    by_evidence = _merge_recs_by_evidence(items)
    chosen: dict[str, RecommendationItem] = {}
    for item in sorted(by_evidence, key=_rec_rank, reverse=True):
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
    """Merge warnings that share evidence, then drop repeated risks."""
    by_evidence = _merge_warns_by_evidence(items)
    chosen: dict[str, WarningItem] = {}
    for item in sorted(by_evidence, key=_warn_rank, reverse=True):
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


def _merge_recs_by_evidence(
    items: tuple[RecommendationItem, ...],
) -> tuple[RecommendationItem, ...]:
    """First collapse recommendations that rest on the same evidence set."""
    ranked = sorted(items, key=_rec_rank, reverse=True)
    chosen: dict[frozenset[str], RecommendationItem] = {}
    for item in ranked:
        key = frozenset(item.evidence_ids) or frozenset({item.recommendation_id})
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


def _merge_warns_by_evidence(items: tuple[WarningItem, ...]) -> tuple[WarningItem, ...]:
    """First collapse warnings that rest on the same evidence set."""
    ranked = sorted(items, key=_warn_rank, reverse=True)
    chosen: dict[frozenset[str], WarningItem] = {}
    for item in ranked:
        key = frozenset(item.evidence_ids) or frozenset({item.warning_id})
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


def _node_rank(node: EvidenceNode) -> tuple[float, float, float, int]:
    """Rank one evidence node."""
    return rank_key(
        node.domain,
        node.importance,
        node.confidence,
        customer_relevance(node.customer_domain, node.engine_truth_ref),
    )


def _rec_rank(item: RecommendationItem) -> tuple[float, float, float, int]:
    """Rank one recommendation."""
    return rank_key(
        item.domain,
        item.importance,
        item.confidence,
        customer_relevance(item.customer_domain),
    )


def _warn_rank(item: WarningItem) -> tuple[float, float, float, int]:
    """Rank one warning."""
    return rank_key(item.domain, item.importance, item.confidence, 0.5)


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
