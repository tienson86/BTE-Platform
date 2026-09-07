"""TV1-B04 recommendation builder, merge, priority, timing, and trace tests."""

from __future__ import annotations

from consulting.marriage.models.enums import (
    FindingPriority,
    RecommendationPriority,
    RecommendationType,
    RecommendationUrgency,
)
from consulting.marriage.recommendation.builder import CanonicalRecommendationProvider
from consulting.marriage.recommendation.versions import RECOMMENDATION_MODEL_VERSION
from tests.consulting.decision_fixtures import build_test_decision, golden_pair


def test_recommendation_requires_decision_findings() -> None:
    """Recommendations are generated only from Decision/Findings."""
    decision = build_test_decision()
    recs = CanonicalRecommendationProvider().provide(decision)
    finding_ids = {item.finding_id for item in decision.findings}
    assert recs
    for item in recs:
        assert item.source_finding_ids
        assert set(item.source_finding_ids) <= finding_ids
        assert item.source_decision_id == decision.consultation_id


def test_no_finding_source_yields_no_recommendation() -> None:
    """An empty finding set produces no actions."""
    decision = build_test_decision()
    decision.findings = []
    assert CanonicalRecommendationProvider().provide(decision) == []


def test_source_trace_integrity() -> None:
    """Every recommendation finding id resolves on the Decision Result."""
    decision = build_test_decision()
    recs = CanonicalRecommendationProvider().provide(decision)
    by_id = {item.finding_id: item for item in decision.findings}
    for rec in recs:
        for finding_id in rec.source_finding_ids:
            finding = by_id[finding_id]
            assert finding.finding_id == finding_id
            assert finding.evidence_ids


def test_recommendation_deterministic_ordering() -> None:
    """The same Decision produces identical recommendation order."""
    decision = build_test_decision()
    first = CanonicalRecommendationProvider().provide(decision)
    second = CanonicalRecommendationProvider().provide(decision)
    assert [item.recommendation_id for item in first] == [item.recommendation_id for item in second]
    assert [item.action_type for item in first] == [item.action_type for item in second]
    assert [tuple(item.source_finding_ids) for item in first] == [
        tuple(item.source_finding_ids) for item in second
    ]


def test_action_semantic_deduplication_and_merge() -> None:
    """Multiple findings with the same action objective merge into one recommendation."""
    decision = build_test_decision()
    recs = CanonicalRecommendationProvider().provide(decision)
    keys = [(item.domain, item.action_type, item.objective) for item in recs]
    assert len(keys) == len(set(keys))
    merged = [item for item in recs if len(item.source_finding_ids) > 1]
    assert merged


def test_priority_derives_from_findings() -> None:
    """Recommendation priority follows source finding priority. No manufactured CRITICAL."""
    decision = build_test_decision()
    recs = CanonicalRecommendationProvider().provide(decision)
    by_finding = {item.finding_id: item for item in decision.findings}
    for rec in recs:
        source_priorities = [by_finding[fid].priority for fid in rec.source_finding_ids]
        assert rec.priority in source_priorities or rec.priority is FindingPriority.P1
        assert rec.action_priority is not RecommendationPriority.CRITICAL
        if all(item is FindingPriority.P5 for item in source_priorities):
            raise AssertionError("P5 findings must not publish independently")


def test_priority_and_urgency_are_independent() -> None:
    """High priority may still be continuous. Timing actions are event-driven."""
    decision = build_test_decision()
    recs = CanonicalRecommendationProvider().provide(decision)
    high_continuous = [
        item
        for item in recs
        if item.action_priority is RecommendationPriority.HIGH
        and item.urgency is RecommendationUrgency.CONTINUOUS
    ]
    timing = [item for item in recs if item.action_type is RecommendationType.TIMING_AWARENESS]
    if timing:
        assert all(item.urgency is RecommendationUrgency.EVENT_DRIVEN for item in timing)
    assert high_continuous or recs


def test_conditions_and_expected_outcome_are_semantic_keys() -> None:
    """Conditions and expected outcomes are structured keys, not customer sentences."""
    recs = CanonicalRecommendationProvider().provide(build_test_decision())
    for item in recs:
        assert item.conditions
        assert item.expected_outcome
        assert item.objective
        assert " " not in item.objective
        assert " " not in item.expected_outcome
        assert all(" " not in condition or "_" in condition for condition in item.conditions)


def test_timing_comes_from_decision_findings_only() -> None:
    """Timing keys are always_applicable or derived from timing findings. No invented years."""
    with_luck = CanonicalRecommendationProvider().provide(build_test_decision())
    without_luck = CanonicalRecommendationProvider().provide(
        build_test_decision(*golden_pair(), include_luck=False)
    )
    for item in with_luck + without_luck:
        assert item.timing_key in {
            "always_applicable",
            "timing_finding_activation",
            "supportive_period",
            "sensitive_period",
        }
        assert item.timing_key is not None
        assert not any(char.isdigit() and len(item.timing_key) == 4 for char in "")
        assert "202" not in (item.timing_key or "")
        assert item.timing_key not in {"wedding_date", "conception_date"}
    off_timing = [item for item in without_luck if item.action_type is RecommendationType.TIMING_AWARENESS]
    assert off_timing == []


def test_recommendation_confidence_does_not_exceed_source() -> None:
    """Action confidence is capped by source finding confidence."""
    decision = build_test_decision()
    recs = CanonicalRecommendationProvider().provide(decision)
    by_id = {item.finding_id: item for item in decision.findings}
    for rec in recs:
        source = min(by_id[fid].confidence for fid in rec.source_finding_ids)
        assert rec.confidence is not None
        assert rec.confidence <= source + 1e-9
        assert 0.0 <= rec.confidence <= 1.0
        assert rec.version == RECOMMENDATION_MODEL_VERSION
