"""Golden decision cases. Factual semantics only. No prose."""

from __future__ import annotations

from consulting.marriage.decision.context import MarriageDecisionContext
from consulting.marriage.decision.resolver import MarriageDecisionResolverV1
from consulting.marriage.evidence.extractor import CanonicalEvidenceBuilder
from consulting.marriage.evidence.resolver import MarriageEvidenceResolver
from consulting.marriage.finding.resolver import CanonicalFindingBuilder
from consulting.marriage.models.context import MarriageRelationshipContext
from consulting.marriage.models.enums import (
    DomainDecisionState,
    MarriageEvidenceType,
    RelationshipSubject,
)
from tests.consulting.decision_fixtures import golden_pair, policy_context_for


def test_golden_decision_semantics() -> None:
    """Golden pair produces stable evidence, findings, domain states, and decision."""
    snapshot_a, snapshot_b = golden_pair()
    context = policy_context_for(snapshot_a, snapshot_b)
    evidence = CanonicalEvidenceBuilder().build_from_policy_context(context)
    resolved = MarriageEvidenceResolver().resolve(evidence)
    findings = CanonicalFindingBuilder().build_from_resolved(evidence, resolved)
    decision_context = MarriageDecisionContext(
        consultation_id=context.consultation_id,
        relationship=MarriageRelationshipContext(
            person_a=snapshot_a,
            person_b=snapshot_b,
            options=context.options,
            available_domains=[],
            limitations=list(context.limitations),
        ),
        versions=context.versions,
        evidence=evidence,
        findings=findings,
    )
    domains = MarriageDecisionResolverV1().resolve_domains(decision_context)
    overall = MarriageDecisionResolverV1().resolve_overall(decision_context)

    types = sorted(item.evidence_type.value for item in evidence)
    assert MarriageEvidenceType.USEFUL_GOD_SUPPORT.value in types
    assert MarriageEvidenceType.BRANCH_CLASH.value in types
    subjects = {
        item.subject
        for item in evidence
        if item.evidence_type is MarriageEvidenceType.USEFUL_GOD_SUPPORT
    }
    assert RelationshipSubject.MUTUAL not in subjects
    assert RelationshipSubject.B_TO_A in subjects

    clash_ids = [
        item.evidence_id
        for item in evidence
        if item.evidence_type is MarriageEvidenceType.BRANCH_CLASH
    ]
    rescued = [
        item
        for item in resolved
        if item.evidence_id in clash_ids
    ]
    assert rescued
    assert findings
    assert all(item.evidence_ids for item in findings)

    assert domains.five_elements.availability.available is True
    assert domains.stem_branch.availability.available is True
    assert domains.family.availability.available is False
    assert domains.family.state is DomainDecisionState.INSUFFICIENT
    assert domains.children.state is DomainDecisionState.INSUFFICIENT
    assert domains.five_elements.score is None
    assert domains.five_elements.grade is None
    assert overall.score is None
    assert overall.grade is None
    assert overall.state is not None
    assert overall.state is not DomainDecisionState.INSUFFICIENT
    assert overall.domain_scores == {}

    signature = (
        tuple((item.evidence_type.value, item.subject.value, item.predicate) for item in evidence),
        tuple((item.finding_id, item.semantic_key, tuple(item.evidence_ids)) for item in findings),
        domains.five_elements.state,
        domains.stem_branch.state,
        overall.state,
    )
    repeat_evidence = CanonicalEvidenceBuilder().build_from_policy_context(context)
    repeat_resolved = MarriageEvidenceResolver().resolve(repeat_evidence)
    repeat_findings = CanonicalFindingBuilder().build_from_resolved(
        repeat_evidence,
        repeat_resolved,
    )
    repeat_context = MarriageDecisionContext(
        consultation_id=context.consultation_id,
        relationship=decision_context.relationship,
        versions=context.versions,
        evidence=repeat_evidence,
        findings=repeat_findings,
    )
    repeat_domains = MarriageDecisionResolverV1().resolve_domains(repeat_context)
    repeat_overall = MarriageDecisionResolverV1().resolve_overall(repeat_context)
    repeat_signature = (
        tuple(
            (item.evidence_type.value, item.subject.value, item.predicate)
            for item in repeat_evidence
        ),
        tuple(
            (item.finding_id, item.semantic_key, tuple(item.evidence_ids))
            for item in repeat_findings
        ),
        repeat_domains.five_elements.state,
        repeat_domains.stem_branch.state,
        repeat_overall.state,
    )
    assert signature == repeat_signature
