"""Opportunity evaluation. Normalized index from amplifying LE-2 overlap."""

from __future__ import annotations

from engines.luck_engine.decision.decision_context import LuckDecisionContext
from engines.luck_engine.decision.decision_models import (
    DecisionEvidence,
    OpportunityScore,
    extract_score_delta,
    iter_stage_impacts,
    mean_or_zero,
)
from engines.luck_engine.decision_constants import IMPACT_OUTPUT_KEYS, OUTPUT_OPPORTUNITY


class OpportunityStage:
    """Publish opportunity_score. Does not write fortune text."""

    stage_id = "opportunity_evaluation"
    dependencies: tuple[str, ...] = ()

    def execute(self, context: LuckDecisionContext) -> dict[str, object]:
        """Map positive deltas × overlap intensity to opportunity_index."""
        impacts = iter_stage_impacts(context.luck_analysis_snapshot)
        components = []
        for impact in impacts:
            score, delta = extract_score_delta(impact)
            components.append(round(score * max(delta, 0.0), 4))
        opportunity = OpportunityScore(mean_or_zero(components))
        evidence = DecisionEvidence(
            impact_keys=tuple(key for key in IMPACT_OUTPUT_KEYS if context.luck_analysis_snapshot.get(key)),
            consumed_fields=("score.value", "delta.value"),
            notes=("amplifying_overlap_only",),
        )
        payload = opportunity.to_dict()
        payload["evidence"] = evidence.to_dict()
        payload["output"] = OUTPUT_OPPORTUNITY
        return payload
