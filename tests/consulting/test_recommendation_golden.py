"""Golden recommendation cases. Structured action semantics only. No prose."""

from __future__ import annotations

from consulting.marriage.models.enums import RecommendationType
from consulting.marriage.recommendation.builder import CanonicalRecommendationProvider
from consulting.marriage.recommendation.versions import RECOMMENDATION_MODEL_VERSION
from consulting.marriage.validation.recommendation import MarriageRecommendationValidation
from tests.consulting.decision_fixtures import build_test_decision


def test_golden_recommendation_semantics() -> None:
    """Golden Decision produces stable structured recommendations."""
    decision = build_test_decision()
    recs = CanonicalRecommendationProvider().provide(decision)
    MarriageRecommendationValidation().validate_recommendations(decision, recs)
    assert recs
    signature = tuple(
        (
            item.recommendation_id,
            item.action_type.value,
            item.objective,
            item.action_priority.value if item.action_priority else None,
            item.urgency.value if item.urgency else None,
            tuple(item.conditions),
            item.timing_key,
            item.expected_outcome,
            round(item.confidence or 0.0, 6),
            tuple(item.source_finding_ids),
            item.version,
        )
        for item in recs
    )
    repeat = CanonicalRecommendationProvider().provide(decision)
    repeat_signature = tuple(
        (
            item.recommendation_id,
            item.action_type.value,
            item.objective,
            item.action_priority.value if item.action_priority else None,
            item.urgency.value if item.urgency else None,
            tuple(item.conditions),
            item.timing_key,
            item.expected_outcome,
            round(item.confidence or 0.0, 6),
            tuple(item.source_finding_ids),
            item.version,
        )
        for item in repeat
    )
    assert signature == repeat_signature
    assert all(item.version == RECOMMENDATION_MODEL_VERSION for item in recs)
    assert all(item.source_finding_ids for item in recs)
    types = {item.action_type for item in recs}
    assert RecommendationType.REDUCE_CONFLICT in types or RecommendationType.REINFORCE_STRENGTH in types
    assert RecommendationType.GENERAL not in types
    for item in recs:
        assert item.narrative_key is None
        assert " " not in (item.objective or "")
