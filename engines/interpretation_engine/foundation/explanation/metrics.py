"""Explainability metrics for Decision Explanation Framework."""

from __future__ import annotations

from engines.interpretation_engine.foundation.explanation.models import (
    DecisionExplanationResult,
    ExplainabilityMetrics,
)


def compute_explainability_metrics(result: DecisionExplanationResult) -> ExplainabilityMetrics:
    """Compute explainability metrics from a decision explanation."""
    evidence_ids = {item.evidence_id for item in result.evidence}
    unsupported = 0

    if result.decision is not None:
        refs = set(result.decision.supporting_evidence_ids)
        if refs and not refs <= evidence_ids:
            unsupported += 1
        elif not refs:
            unsupported += 1

    total_refs = 0
    covered_refs = 0
    if result.decision is not None:
        for ref in result.decision.supporting_evidence_ids:
            total_refs += 1
            if ref in evidence_ids:
                covered_refs += 1

    ratio = covered_refs / total_refs if total_refs else 1.0

    return ExplainabilityMetrics(
        fact_count=len(result.analysis),
        decision_step_count=len(result.decision_path),
        evidence_count=len(result.evidence),
        alternative_count=len(result.alternatives),
        evidence_coverage_ratio=round(ratio, 4),
        unsupported_decision_count=unsupported,
    )
