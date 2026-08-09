"""Confidence evaluation from LE-2 impact completeness and upstream success flags."""

from __future__ import annotations

from engines.luck_engine.decision.decision_context import LuckDecisionContext
from engines.luck_engine.decision.decision_models import DecisionConfidence, iter_stage_impacts, min_confidence
from engines.luck_engine.decision_constants import (
    CONFIDENCE_LOW,
    CONFIDENCE_NONE,
    OUTPUT_CONFIDENCE,
    OUTPUT_OPPORTUNITY,
    OUTPUT_RISK,
)
from engines.luck_engine.exceptions import LuckDecisionDependencyError

_RANK = {"none": 0, "low": 1, "medium": 2, "high": 3}


def _cap(label: str, ceiling: str) -> str:
    if _RANK.get(label, 0) > _RANK.get(ceiling, 0):
        return ceiling
    return label


class ConfidenceStage:
    """Publish decision_confidence. Completeness only — not certainty of fortune."""

    stage_id = "confidence_evaluation"
    dependencies: tuple[str, ...] = (OUTPUT_OPPORTUNITY, OUTPUT_RISK)

    def execute(self, context: LuckDecisionContext) -> dict[str, object]:
        """Derive confidence from impact labels and upstream success flags."""
        missing = [name for name in self.dependencies if not context.has_published(name)]
        if missing:
            raise LuckDecisionDependencyError(f"missing_inputs:{self.stage_id}:{','.join(missing)}")
        impacts = iter_stage_impacts(context.luck_analysis_snapshot)
        labels = []
        for impact in impacts:
            block = impact.get("confidence") if isinstance(impact.get("confidence"), dict) else {}
            labels.append(str(block.get("value") or CONFIDENCE_NONE))
        value = min_confidence(labels)
        luck_ok = bool(context.luck_analysis_snapshot.get("success"))
        analysis_ok = bool(context.analysis_snapshot.get("success"))
        decision_ok = bool(context.decision_snapshot.get("success"))
        if not luck_ok or not analysis_ok or not decision_ok:
            value = _cap(value, CONFIDENCE_LOW)
        confidence = DecisionConfidence(value)
        payload = confidence.to_dict()
        payload["output"] = OUTPUT_CONFIDENCE
        payload["consumed"] = {
            "luck_analysis_success": luck_ok,
            "analysis_success": analysis_ok,
            "decision_success": decision_ok,
            "impact_count": len(impacts),
        }
        return payload
