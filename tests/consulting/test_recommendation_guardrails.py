"""TV1-B04 recommendation graph, guardrails, and missing-data tests."""

from __future__ import annotations

from consulting.marriage.models.enums import (
    CanonicalGender,
    FindingPriority,
    FiveElement,
    MarriageDomain,
    PersonSide,
    RecommendationPriority,
)
from consulting.marriage.models.snapshot import ShenShaItem
from consulting.marriage.recommendation.builder import CanonicalRecommendationProvider
from consulting.marriage.recommendation.graph import assert_graph
from tests.consulting.decision_fixtures import build_test_decision, golden_pair, make_snapshot


def test_recommendation_graph_has_no_orphan_or_cycle() -> None:
    """Published actions have source findings and acyclic dependencies."""
    recs = CanonicalRecommendationProvider().provide(build_test_decision())
    assert_graph(recs)
    ids = {item.recommendation_id for item in recs}
    for item in recs:
        assert item.source_finding_ids
        assert set(item.depends_on) <= ids
        assert item.recommendation_id not in item.depends_on


def test_secondary_evidence_cannot_publish_high_priority_action() -> None:
    """Shen Sha / Cung Phi cannot independently generate HIGH or CRITICAL actions."""
    snapshot_a, snapshot_b = golden_pair()
    assert snapshot_a.shen_sha is not None
    snapshot_a.shen_sha.items.extend(
        [
            ShenShaItem(name="Ky Than", polarity="negative"),
            ShenShaItem(name="Co Than", polarity="inauspicious"),
        ]
    )
    decision = build_test_decision(snapshot_a, snapshot_b)
    recs = CanonicalRecommendationProvider().provide(decision)
    p5_ids = {item.finding_id for item in decision.findings if item.priority is FindingPriority.P5}
    for rec in recs:
        assert rec.action_priority is not RecommendationPriority.CRITICAL
        if set(rec.source_finding_ids) <= p5_ids:
            raise AssertionError("secondary findings published independently")
        assert rec.priority is not FindingPriority.P5


def test_missing_domain_does_not_fabricate_recommendation() -> None:
    """Insufficient family/children/interaction domains produce no fake actions."""
    decision = build_test_decision()
    recs = CanonicalRecommendationProvider().provide(decision)
    blocked = {
        MarriageDomain.FAMILY,
        MarriageDomain.CHILDREN,
        MarriageDomain.INTERACTION,
    }
    assert decision.domains.family.availability.available is False
    assert decision.domains.children.availability.available is False
    assert all(item.domain not in blocked for item in recs)


def test_missing_birth_hour_does_not_generate_negative_advice() -> None:
    """Missing hour may lower confidence. It does not add a penalty action."""
    snapshot_a, snapshot_b = golden_pair()
    known = CanonicalRecommendationProvider().provide(build_test_decision(snapshot_a, snapshot_b))
    missing_a = make_snapshot(
        analysis_id="MC-GOLDEN-A",
        side=PersonSide.A,
        gender=CanonicalGender.MALE,
        day_stem="Canh",
        day_branch="Tý",
        day_element=FiveElement.METAL,
        useful=FiveElement.FIRE,
        hour_known=False,
        luck_stem="Quý",
        luck_branch="Hợi",
    )
    missing = CanonicalRecommendationProvider().provide(build_test_decision(missing_a, snapshot_b))
    known_types = {(item.domain, item.action_type, item.objective) for item in known}
    missing_types = {(item.domain, item.action_type, item.objective) for item in missing}
    assert missing_types <= known_types
    if known and missing:
        assert min(item.confidence or 0.0 for item in missing) <= min(
            item.confidence or 0.0 for item in known
        ) + 1e-9


def test_no_customer_prose_in_recommendations() -> None:
    """Canonical recommendation output stays structured."""
    recs = CanonicalRecommendationProvider().provide(build_test_decision())
    blob = " ".join(
        filter(
            None,
            [
                *(item.objective or "" for item in recs),
                *(item.expected_outcome or "" for item in recs),
                *(item.technical_reason or "" for item in recs),
                *(item.narrative_key or "" for item in recs),
            ],
        )
    ).lower()
    for phrase in ("hai bạn", "vợ chồng cần", "hai người rất hợp", "must marry", "must not marry"):
        assert phrase not in blob
    for item in recs:
        assert item.narrative_key is None


def test_recommendation_does_not_change_decision() -> None:
    """Building actions does not mutate Decision state, score, or findings."""
    decision = build_test_decision()
    state = decision.overall.state
    score = decision.overall.score
    finding_ids = [item.finding_id for item in decision.findings]
    evidence_ids = [item.evidence_id for item in decision.evidence]
    CanonicalRecommendationProvider().provide(decision)
    assert decision.overall.state is state
    assert decision.overall.score is score
    assert decision.overall.grade is None
    assert [item.finding_id for item in decision.findings] == finding_ids
    assert [item.evidence_id for item in decision.evidence] == evidence_ids
    assert decision.recommendations == []


def test_score_remains_unavailable() -> None:
    """B04 does not invent compatibility score or grade."""
    decision = build_test_decision()
    recs = CanonicalRecommendationProvider().provide(decision)
    assert decision.overall.score is None
    assert decision.overall.grade is None
    assert recs
    assert all(item.action_type is not None for item in recs)
