"""Decision publication. Structured reasons and overall payload only."""

from __future__ import annotations

from engines.luck_engine.decision.decision_context import LuckDecisionContext
from engines.luck_engine.decision.decision_models import (
    DecisionReason,
    DecisionSummary,
    iter_stage_impacts,
)
from engines.luck_engine.decision_constants import (
    DECISION_VERSION,
    OUTPUT_CONFIDENCE,
    OUTPUT_OPPORTUNITY,
    OUTPUT_OVERALL,
    OUTPUT_PRIORITY,
    OUTPUT_REASONING,
    OUTPUT_RISK,
    OUTPUT_VERSION,
    REASON_CNF,
    REASON_OPP,
    REASON_PRI,
    REASON_PUB,
    REASON_RSK,
)
from engines.luck_engine.exceptions import LuckDecisionDependencyError


def _value(payload: object) -> object:
    if isinstance(payload, dict):
        return payload.get("value")
    return None


class PublicationStage:
    """Publish reasoning, overall decision, and decision_version."""

    stage_id = "decision_publication"
    dependencies: tuple[str, ...] = (OUTPUT_PRIORITY,)

    def execute(self, context: LuckDecisionContext) -> dict[str, object]:
        """Assemble structured publication fields. No narrative text."""
        missing = [name for name in self.dependencies if not context.has_published(name)]
        if missing:
            raise LuckDecisionDependencyError(f"missing_inputs:{self.stage_id}:{','.join(missing)}")
        opportunity = context.get_published(OUTPUT_OPPORTUNITY) or {}
        risk = context.get_published(OUTPUT_RISK) or {}
        confidence = context.get_published(OUTPUT_CONFIDENCE) or {}
        priority = context.get_published(OUTPUT_PRIORITY) or {}
        reasons = [
            DecisionReason(REASON_OPP, (OUTPUT_OPPORTUNITY,), _value(opportunity)).to_dict(),
            DecisionReason(REASON_RSK, (OUTPUT_RISK,), _value(risk)).to_dict(),
            DecisionReason(REASON_CNF, (OUTPUT_CONFIDENCE,), _value(confidence)).to_dict(),
            DecisionReason(REASON_PRI, (OUTPUT_PRIORITY,), _value(priority)).to_dict(),
            DecisionReason(REASON_PUB, (OUTPUT_OVERALL, OUTPUT_VERSION), DECISION_VERSION).to_dict(),
        ]
        summary = DecisionSummary(
            opportunity_value=float(_value(opportunity) or 0.0),
            risk_value=float(_value(risk) or 0.0),
            priority_value=str(_value(priority) or ""),
            confidence_value=str(_value(confidence) or ""),
            impact_count=len(iter_stage_impacts(context.luck_analysis_snapshot)),
        )
        overall = {
            "opportunity_score": opportunity,
            "risk_score": risk,
            "luck_priority": priority,
            "decision_confidence": confidence,
            "summary": summary.to_dict(),
            "decision_version": DECISION_VERSION,
        }
        return {
            OUTPUT_REASONING: reasons,
            OUTPUT_OVERALL: overall,
            OUTPUT_VERSION: DECISION_VERSION,
        }
