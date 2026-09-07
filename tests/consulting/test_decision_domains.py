"""TV1-B03 domain availability, missing-hour, secondary, and luck tests."""

from __future__ import annotations

from consulting.marriage.decision.context import MarriageDecisionContext
from consulting.marriage.decision.resolver import MarriageDecisionResolverV1
from consulting.marriage.evidence.extractor import CanonicalEvidenceBuilder
from consulting.marriage.evidence.resolver import MarriageEvidenceResolver
from consulting.marriage.finding.resolver import CanonicalFindingBuilder
from consulting.marriage.models.context import MarriageRelationshipContext
from consulting.marriage.models.enums import (
    CanonicalGender,
    DomainDecisionState,
    FiveElement,
    MarriageDomain,
    MarriageEvidenceType,
    PersonSide,
)
from consulting.marriage.models.snapshot import ShenShaItem
from tests.consulting.decision_fixtures import (
    golden_pair,
    make_snapshot,
    policy_context_for,
)


def _decide(context):
    evidence = CanonicalEvidenceBuilder().build_from_policy_context(context)
    resolved = MarriageEvidenceResolver().resolve(evidence)
    findings = CanonicalFindingBuilder().build_from_resolved(evidence, resolved)
    decision_context = MarriageDecisionContext(
        consultation_id=context.consultation_id,
        relationship=MarriageRelationshipContext(
            person_a=context.snapshot_a,
            person_b=context.snapshot_b,
            options=context.options,
            available_domains=list(context.available_domains),
            limitations=list(context.limitations),
        ),
        versions=context.versions,
        evidence=evidence,
        findings=findings,
    )
    domains = MarriageDecisionResolverV1().resolve_domains(decision_context)
    overall = MarriageDecisionResolverV1().resolve_overall(decision_context)
    return evidence, domains, overall, decision_context


def test_unavailable_domains_are_insufficient() -> None:
    """Family and children stay insufficient when no primary evidence exists."""
    snapshot_a, snapshot_b = golden_pair()
    _evidence, domains, _overall, _ctx = _decide(policy_context_for(snapshot_a, snapshot_b))
    assert domains.family.availability.available is False
    assert domains.family.state is DomainDecisionState.INSUFFICIENT
    assert domains.family.score is None
    assert domains.family.grade is None
    assert domains.children.availability.available is False
    assert domains.children.state is DomainDecisionState.INSUFFICIENT
    assert domains.interaction.availability.available is False


def test_missing_birth_hour_is_not_a_compatibility_penalty() -> None:
    """Missing hour lowers completeness/confidence, not a hidden negative score."""
    snapshot_a, snapshot_b = golden_pair()
    snapshot_a = make_snapshot(
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
    known = policy_context_for(*golden_pair())
    missing = policy_context_for(snapshot_a, snapshot_b)
    _e1, d1, o1, _c1 = _decide(known)
    _e2, d2, o2, _c2 = _decide(missing)
    assert o1.score is None and o2.score is None
    assert d1.five_elements.score is None and d2.five_elements.score is None
    hour_evidence = [
        item
        for item in _e2
        if any("pillars.hour" in ref.path for ref in item.source_refs)
    ]
    assert hour_evidence == []
    assert "birth_time_unknown" in missing.limitations


def test_secondary_evidence_cannot_dominate_structural_state() -> None:
    """Shen Sha / Cung Phi cannot flip a supportive Tier 1 overall state."""
    snapshot_a, snapshot_b = golden_pair()
    assert snapshot_a.shen_sha is not None
    snapshot_a.shen_sha.items.extend(
        [
            ShenShaItem(name="Ky Than", polarity="negative"),
            ShenShaItem(name="Co Than", polarity="inauspicious"),
        ]
    )
    evidence, domains, overall, _ctx = _decide(policy_context_for(snapshot_a, snapshot_b))
    secondary = [
        item
        for item in evidence
        if item.evidence_type
        in {
            MarriageEvidenceType.SHEN_SHA_SUPPORT,
            MarriageEvidenceType.SHEN_SHA_RISK,
            MarriageEvidenceType.FENG_SHUI_REFERENCE,
        }
    ]
    assert secondary
    assert domains.five_elements.state is not DomainDecisionState.INSUFFICIENT
    assert overall.state is not DomainDecisionState.CRITICAL
    assert overall.state in {
        DomainDecisionState.SUPPORTIVE,
        DomainDecisionState.MIXED,
        DomainDecisionState.PRESSURED,
        DomainDecisionState.BALANCED,
    }
    structural = domains.five_elements.state
    assert structural != DomainDecisionState.INSUFFICIENT
    p5 = [item for item in domains.five_elements.findings if item.priority.value == "P5"]
    assert p5
    assert overall.state is not None


def test_luck_is_activation_not_natal_rewrite() -> None:
    """Luck misalignment cannot rewrite a natal overall state."""
    snapshot_a, snapshot_b = golden_pair()
    with_luck = policy_context_for(snapshot_a, snapshot_b, include_luck=True)
    without_luck = policy_context_for(snapshot_a, snapshot_b, include_luck=False)
    evidence_luck, domains_luck, overall_luck, _c1 = _decide(with_luck)
    _evidence_off, domains_off, overall_off, _c2 = _decide(without_luck)
    luck_atoms = [
        item
        for item in evidence_luck
        if item.domain is MarriageDomain.LUCK
    ]
    assert overall_luck.state == overall_off.state
    assert domains_off.luck.availability.available is False
    assert domains_off.luck.state is DomainDecisionState.INSUFFICIENT
    if luck_atoms:
        assert domains_luck.luck.availability.available is True
        assert all(item.scope == "timing" for item in luck_atoms)
        assert all(item.significance.value == "minor" for item in luck_atoms)
