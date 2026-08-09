"""Risk evaluation. Normalized index from dampening LE-2 overlap."""

from __future__ import annotations

from engines.luck_engine.decision.decision_context import LuckDecisionContext
from engines.luck_engine.decision.decision_models import (
    DecisionEvidence,
    RiskScore,
    extract_score_delta,
    iter_stage_impacts,
    mean_or_zero,
)
from engines.luck_engine.decision_constants import IMPACT_OUTPUT_KEYS, OUTPUT_OPPORTUNITY, OUTPUT_RISK
from engines.luck_engine.exceptions import LuckDecisionDependencyError


class RiskStage:
    """Publish risk_score. Does not write fortune text."""

    stage_id = "risk_evaluation"
    dependencies: tuple[str, ...] = (OUTPUT_OPPORTUNITY,)

    def execute(self, context: LuckDecisionContext) -> dict[str, object]:
        """Map negative deltas × overlap intensity to risk_index."""
        missing = [name for name in self.dependencies if not context.has_published(name)]
        if missing:
            raise LuckDecisionDependencyError(f"missing_inputs:{self.stage_id}:{','.join(missing)}")
        impacts = iter_stage_impacts(context.luck_analysis_snapshot)
        components = []
        for impact in impacts:
            score, delta = extract_score_delta(impact)
            components.append(round(score * max(-delta, 0.0), 4))
        risk = RiskScore(mean_or_zero(components))
        evidence = DecisionEvidence(
            impact_keys=tuple(key for key in IMPACT_OUTPUT_KEYS if context.luck_analysis_snapshot.get(key)),
            consumed_fields=("score.value", "delta.value", OUTPUT_OPPORTUNITY),
            notes=("dampening_overlap_only",),
        )
        payload = risk.to_dict()
        payload["evidence"] = evidence.to_dict()
        payload["output"] = OUTPUT_RISK
        return payload
