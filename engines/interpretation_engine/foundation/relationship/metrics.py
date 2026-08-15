"""Explainability metrics for Relationship Reasoning Framework."""

from __future__ import annotations

from engines.interpretation_engine.foundation.relationship.models import (
    RelationshipAssessment,
    RelationshipMetrics,
)


def compute_relationship_metrics(assessment: RelationshipAssessment) -> RelationshipMetrics:
    """Compute graph and evidence-coverage metrics from an assessment."""
    evidence_ids = {item.evidence_id for item in assessment.evidence}
    supported = 0
    unsupported = 0
    total_refs = 0
    covered_refs = 0
    for edge in assessment.graph.edges:
        refs = tuple(item for item in edge.evidence_ids if item)
        if refs and set(refs) <= evidence_ids:
            supported += 1
        else:
            unsupported += 1
        for ref in refs:
            total_refs += 1
            if ref in evidence_ids:
                covered_refs += 1
    coverage = covered_refs / total_refs if total_refs else 0.0
    return RelationshipMetrics(
        node_count=len(assessment.graph.nodes),
        edge_count=len(assessment.graph.edges),
        supported_relationships=supported,
        unsupported_relationships=unsupported,
        evidence_coverage=round(coverage, 4),
    )
