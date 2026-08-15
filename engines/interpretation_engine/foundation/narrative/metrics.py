"""Composer metrics — coverage of evidence, reasons, recommendations, warnings, trace."""

from __future__ import annotations

from engines.interpretation_engine.foundation.narrative.models import (
    ComposerMetrics,
    EvidenceGraph,
    EvidenceNode,
    NarrativeSection,
    RecommendationItem,
    ReasoningChain,
    TraceabilityRecord,
    WarningItem,
)


def build_metrics(
    *,
    graph: EvidenceGraph,
    chains: tuple[ReasoningChain, ...],
    recommendations: tuple[RecommendationItem, ...],
    warnings: tuple[WarningItem, ...],
    sections: tuple[NarrativeSection, ...],
    traceability: tuple[TraceabilityRecord, ...],
) -> ComposerMetrics:
    """Compute composition coverage. Does not score astrology."""
    sentences = tuple(sentence for section in sections for sentence in section.sentences)
    used_nodes = _canonical_nodes(graph, sentences)
    used_ids = {node.evidence_id for node in used_nodes}
    chain_ids = {chain.reason_id for chain in chains} | {
        chain.conclusion_id for chain in chains
    }
    used_reasons = used_ids & chain_ids
    rec_used = sum(
        1
        for item in recommendations
        if _canonical_ids(graph, item.evidence_ids) & used_ids
    )
    warn_used = sum(
        1
        for item in warnings
        if _canonical_ids(graph, item.evidence_ids) & used_ids
    )
    orphans = sum(1 for record in traceability if not record.evidence_ids)
    raw = max(graph.raw_count, 0)
    merged = max(graph.merged_count, 0)
    duplicate_ratio = ((raw - merged) / raw) if raw else 0.0
    return ComposerMetrics(
        evidence_coverage=_ratio(len(used_ids), len(graph.nodes)),
        duplicate_ratio=max(duplicate_ratio, 0.0),
        reason_coverage=_ratio(len(used_reasons), len(chains)),
        recommendation_coverage=_ratio(rec_used, len(recommendations)),
        warning_coverage=_ratio(warn_used, len(warnings)),
        traceability_coverage=_ratio(len(traceability) - orphans, len(traceability)),
        evidence_count=len(graph.nodes),
        sentence_count=len(sentences),
        orphan_sentence_count=orphans,
    )


def _canonical_nodes(graph: EvidenceGraph, sentences) -> set[EvidenceNode]:
    """Resolve sentence evidence ids onto surviving graph nodes."""
    found: set[EvidenceNode] = set()
    for sentence in sentences:
        for evidence_id in sentence.evidence_ids:
            node = graph.get(evidence_id)
            if node is not None:
                found.add(node)
    return found


def _canonical_ids(graph: EvidenceGraph, evidence_ids: tuple[str, ...]) -> set[str]:
    """Map possibly-aliased evidence ids to surviving node ids."""
    resolved: set[str] = set()
    for evidence_id in evidence_ids:
        node = graph.get(evidence_id)
        if node is not None:
            resolved.add(node.evidence_id)
    return resolved


def _ratio(numerator: int, denominator: int) -> float:
    """Safe coverage ratio in [0, 1]."""
    if denominator <= 0:
        return 1.0
    return min(numerator / denominator, 1.0)
