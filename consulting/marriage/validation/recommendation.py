"""TV1-B04 recommendation validation. Does not replace B03 decision validation."""

from __future__ import annotations

from consulting.marriage.exceptions import MarriageRecommendationError
from consulting.marriage.models.enums import (
    RecommendationPriority,
    RecommendationType,
    RecommendationUrgency,
)
from consulting.marriage.models.recommendation import MarriageRecommendation
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.recommendation.graph import assert_graph
from consulting.marriage.validation.decision import MarriageDecisionValidation

_FORBIDDEN = (
    "must marry",
    "must not marry",
    "hai bạn",
    "vợ chồng cần",
    "hai người rất hợp",
    "certain divorce",
    "infidelity",
    "infertile",
    "guaranteed wealth",
)


class MarriageRecommendationValidation(MarriageDecisionValidation):
    """Validate structured recommendations after Decision is already validated."""

    def validate_recommendations(
        self,
        decision: MarriageDecisionResult,
        recommendations: list[MarriageRecommendation],
    ) -> None:
        """Fail closed when a recommendation cannot be traced to Decision/Findings."""
        finding_ids = {item.finding_id for item in decision.findings}
        seen: set[str] = set()
        for item in recommendations:
            _validate_one(item, decision.consultation_id, finding_ids, seen)
        assert_graph(recommendations)
        if decision.overall.score is not None or decision.overall.grade is not None:
            raise MarriageRecommendationError("score_must_remain_unavailable")


def _validate_one(
    item: MarriageRecommendation,
    consultation_id: str,
    finding_ids: set[str],
    seen: set[str],
) -> None:
    """Validate one recommendation contract."""
    if not item.recommendation_id:
        raise MarriageRecommendationError("recommendation_id_missing")
    if item.recommendation_id in seen:
        raise MarriageRecommendationError(f"recommendation_id_duplicate:{item.recommendation_id}")
    seen.add(item.recommendation_id)
    if not item.source_finding_ids:
        raise MarriageRecommendationError(f"recommendation_source_missing:{item.recommendation_id}")
    for finding_id in item.source_finding_ids:
        if finding_id not in finding_ids:
            raise MarriageRecommendationError(
                f"recommendation_finding_unresolved:{item.recommendation_id}:{finding_id}"
            )
    if item.action_type not in RecommendationType:
        raise MarriageRecommendationError(f"invalid_action_type:{item.recommendation_id}")
    if not item.objective:
        raise MarriageRecommendationError(f"objective_missing:{item.recommendation_id}")
    if item.action_priority not in RecommendationPriority:
        raise MarriageRecommendationError(f"priority_missing:{item.recommendation_id}")
    if item.urgency not in RecommendationUrgency:
        raise MarriageRecommendationError(f"urgency_missing:{item.recommendation_id}")
    if not item.conditions:
        raise MarriageRecommendationError(f"conditions_missing:{item.recommendation_id}")
    if item.confidence is None or not 0.0 <= item.confidence <= 1.0:
        raise MarriageRecommendationError(f"confidence_invalid:{item.recommendation_id}")
    if not item.version:
        raise MarriageRecommendationError(f"version_missing:{item.recommendation_id}")
    if item.source_decision_id != consultation_id:
        raise MarriageRecommendationError(f"source_decision_mismatch:{item.recommendation_id}")
    if item.narrative_key:
        raise MarriageRecommendationError(f"narrative_not_allowed:{item.recommendation_id}")
    _reject_prose(item.objective)
    _reject_prose(item.expected_outcome)
    _reject_prose(item.technical_reason)


def _reject_prose(value: str | None) -> None:
    """Reject customer-facing sentences and hard conclusions."""
    if not value:
        return
    lowered = value.lower()
    if " " in value.strip() and any(token in lowered for token in ("nên", "cần", "hãy")):
        raise MarriageRecommendationError("customer_prose_not_allowed")
    for phrase in _FORBIDDEN:
        if phrase in lowered:
            raise MarriageRecommendationError(f"forbidden_conclusion:{phrase}")
