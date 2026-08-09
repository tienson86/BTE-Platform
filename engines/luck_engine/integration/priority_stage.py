"""Priority resolution. Legal class from opportunity vs risk vs confidence."""

from __future__ import annotations

from engines.luck_engine.decision.decision_context import LuckDecisionContext
from engines.luck_engine.decision.decision_models import DecisionPriority
from engines.luck_engine.decision_constants import (
    CONFIDENCE_NONE,
    OUTPUT_CONFIDENCE,
    OUTPUT_OPPORTUNITY,
    OUTPUT_PRIORITY,
    OUTPUT_RISK,
    PRIORITY_BALANCED,
    PRIORITY_MARGIN,
    PRIORITY_OPPORTUNITY_FIRST,
    PRIORITY_RISK_FIRST,
    PRIORITY_WITHHELD,
)
from engines.luck_engine.exceptions import LuckDecisionDependencyError


def _score_value(payload: object) -> float:
    if isinstance(payload, dict):
        return float(payload.get("value") or 0.0)
    return 0.0


def _confidence_value(payload: object) -> str:
    if isinstance(payload, dict):
        return str(payload.get("value") or CONFIDENCE_NONE)
    return CONFIDENCE_NONE


class PriorityStage:
    """Publish luck_priority. Withheld when confidence is none."""

    stage_id = "priority_resolution"
    dependencies: tuple[str, ...] = (OUTPUT_OPPORTUNITY, OUTPUT_RISK, OUTPUT_CONFIDENCE)

    def execute(self, context: LuckDecisionContext) -> dict[str, object]:
        """Compare opportunity and risk indexes into a legal priority class."""
        missing = [name for name in self.dependencies if not context.has_published(name)]
        if missing:
            raise LuckDecisionDependencyError(f"missing_inputs:{self.stage_id}:{','.join(missing)}")
        opportunity = _score_value(context.get_published(OUTPUT_OPPORTUNITY))
        risk = _score_value(context.get_published(OUTPUT_RISK))
        confidence = _confidence_value(context.get_published(OUTPUT_CONFIDENCE))
        if confidence == CONFIDENCE_NONE:
            priority = PRIORITY_WITHHELD
        elif abs(opportunity - risk) < PRIORITY_MARGIN:
            priority = PRIORITY_BALANCED
        elif opportunity > risk:
            priority = PRIORITY_OPPORTUNITY_FIRST
        else:
            priority = PRIORITY_RISK_FIRST
        payload = DecisionPriority(priority).to_dict()
        payload["output"] = OUTPUT_PRIORITY
        payload["compared"] = {"opportunity": opportunity, "risk": risk, "margin": PRIORITY_MARGIN}
        return payload
