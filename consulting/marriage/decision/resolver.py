"""Domain and overall semantic decision. Score projection is unavailable."""

from __future__ import annotations

from consulting.marriage.decision.contract import MarriageDecisionResolver
from consulting.marriage.decision.context import MarriageDecisionContext
from consulting.marriage.models.confidence import MarriageConfidenceResult
from consulting.marriage.models.decision import (
    DomainAvailability,
    MarriageDomainDecision,
    MarriageDomainResults,
    MarriageOverallDecision,
)
from consulting.marriage.models.enums import (
    ConfidenceLevel,
    DomainDecisionState,
    FindingPriority,
    FindingRelation,
    FindingType,
    MarriageDomain,
)
from consulting.marriage.models.evidence import MarriageEvidence
from consulting.marriage.models.finding import FindingReference, MarriageFinding
from consulting.marriage.policy.v1 import domain_policy, load_marriage_policy_v1

_TIER1 = (
    MarriageDomain.FIVE_ELEMENTS,
    MarriageDomain.STEM_BRANCH,
    MarriageDomain.TEN_GODS,
)
_DOMAIN_ORDER = (
    MarriageDomain.FIVE_ELEMENTS,
    MarriageDomain.STEM_BRANCH,
    MarriageDomain.TEN_GODS,
    MarriageDomain.INTERACTION,
    MarriageDomain.FINANCE,
    MarriageDomain.FAMILY,
    MarriageDomain.CHILDREN,
    MarriageDomain.LUCK,
)


class MarriageDecisionResolverV1(MarriageDecisionResolver):
    """Resolve domain and overall semantic states from findings."""

    def resolve_domains(self, context: MarriageDecisionContext) -> MarriageDomainResults:
        """Resolve each V1 domain from findings and resolved evidence."""
        decisions = {
            domain: _domain_decision(domain, context)
            for domain in _DOMAIN_ORDER
        }
        _apply_cross_domain(decisions)
        return MarriageDomainResults(
            five_elements=decisions[MarriageDomain.FIVE_ELEMENTS],
            stem_branch=decisions[MarriageDomain.STEM_BRANCH],
            ten_gods=decisions[MarriageDomain.TEN_GODS],
            interaction=decisions[MarriageDomain.INTERACTION],
            finance=decisions[MarriageDomain.FINANCE],
            family=decisions[MarriageDomain.FAMILY],
            children=decisions[MarriageDomain.CHILDREN],
            luck=decisions[MarriageDomain.LUCK],
        )

    def resolve_overall(self, context: MarriageDecisionContext) -> MarriageOverallDecision:
        """Resolve overall semantic state from Tier 1. Score stays unavailable."""
        domains = context.relationship
        _ = domains
        domain_results = self.resolve_domains(context)
        tier1 = [
            domain_results.five_elements,
            domain_results.stem_branch,
            domain_results.ten_gods,
        ]
        state = _overall_state(tier1)
        findings = context.findings
        return MarriageOverallDecision(
            score=None,
            grade=None,
            confidence=_overall_confidence(context, tier1),
            headline_finding_ids=_headline_ids(findings),
            strength_finding_ids=[item.finding_id for item in findings if item.type is FindingType.SUPPORT],
            risk_finding_ids=[item.finding_id for item in findings if item.type is FindingType.RISK],
            condition_finding_ids=[
                item.finding_id for item in findings if item.type is FindingType.CONDITION
            ],
            domain_scores={},
            state=state,
        )


def build_confidence(
    *,
    data_quality: float,
    evidence: list[MarriageEvidence],
    limitations: list[str],
    engine_coverage: float,
) -> MarriageConfidenceResult:
    """Confidence is independent of compatibility score."""
    if evidence:
        evidence_quality = sum(item.confidence for item in evidence) / len(evidence)
    else:
        evidence_quality = 0.0
    overall = min(data_quality, evidence_quality if evidence else data_quality, engine_coverage)
    if overall >= 0.8:
        level = ConfidenceLevel.HIGH
    elif overall >= 0.5:
        level = ConfidenceLevel.MEDIUM
    else:
        level = ConfidenceLevel.REFERENCE_ONLY
    return MarriageConfidenceResult(
        overall=overall,
        data_quality=data_quality,
        evidence_quality=evidence_quality,
        engine_coverage=engine_coverage,
        level=level,
        limitations=list(limitations),
    )


def _domain_decision(domain: MarriageDomain, context: MarriageDecisionContext) -> MarriageDomainDecision:
    """Resolve one domain. Missing primary evidence is insufficient, not balanced."""
    policy = domain_policy(load_marriage_policy_v1(), domain)
    findings = [item for item in context.findings if item.domain is domain]
    evidence = [item for item in context.evidence if item.domain is domain]
    primary = [
        item
        for item in evidence
        if item.evidence_type in policy.primary_types and item.scope != "reference"
    ]
    structural_findings = [
        item for item in findings if item.priority not in {FindingPriority.P4, FindingPriority.P5}
    ]
    available = bool(primary)
    reason = None if available else "primary_evidence_unavailable"
    missing = None if available else [domain.value]
    state = (
        _state_from_findings(structural_findings, primary)
        if available
        else DomainDecisionState.INSUFFICIENT
    )
    if domain is MarriageDomain.LUCK and not available:
        reason = "luck_activation_unavailable"
    return MarriageDomainDecision(
        domain=domain,
        availability=DomainAvailability(
            available=available,
            reason=reason,
            required_fields_missing=missing,
        ),
        confidence=_mean_confidence(primary or evidence),
        findings=findings,
        evidence_ids=[item.evidence_id for item in evidence],
        score=None,
        grade=None,
        state=state,
        cross_domain_refs=[],
    )


def _state_from_findings(
    findings: list[MarriageFinding],
    primary: list[MarriageEvidence],
) -> DomainDecisionState:
    """Map support/risk findings onto a structural state."""
    if not primary:
        return DomainDecisionState.INSUFFICIENT
    support = [item for item in findings if item.type is FindingType.SUPPORT]
    risk = [item for item in findings if item.type is FindingType.RISK]
    mixed = [item for item in findings if item.type is FindingType.MIXED]
    if support and not risk and not mixed:
        return DomainDecisionState.SUPPORTIVE
    if risk and not support:
        if any(item.priority is FindingPriority.P0 for item in risk):
            return DomainDecisionState.CRITICAL
        return DomainDecisionState.PRESSURED
    if support and risk:
        return DomainDecisionState.MIXED
    if mixed:
        return DomainDecisionState.MIXED
    if findings:
        return DomainDecisionState.BALANCED
    return DomainDecisionState.INSUFFICIENT


def _overall_state(tier1: list[MarriageDomainDecision]) -> DomainDecisionState:
    """Overall follows Tier 1 only. Luck and secondary cannot rewrite natal."""
    available = [item for item in tier1 if item.availability.available and item.state is not None]
    if not available:
        return DomainDecisionState.INSUFFICIENT
    states = [item.state for item in available if item.state is not None]
    if DomainDecisionState.CRITICAL in states:
        return DomainDecisionState.CRITICAL
    if all(state is DomainDecisionState.SUPPORTIVE for state in states):
        return DomainDecisionState.SUPPORTIVE
    if all(state in {DomainDecisionState.PRESSURED, DomainDecisionState.CRITICAL} for state in states):
        return DomainDecisionState.PRESSURED
    if DomainDecisionState.MIXED in states or len(set(states)) > 1:
        if DomainDecisionState.SUPPORTIVE in states and DomainDecisionState.PRESSURED in states:
            return DomainDecisionState.MIXED
        if DomainDecisionState.SUPPORTIVE in states and DomainDecisionState.INSUFFICIENT in states:
            return DomainDecisionState.SUPPORTIVE
        return DomainDecisionState.MIXED
    return states[0]


def _apply_cross_domain(decisions: dict[MarriageDomain, MarriageDomainDecision]) -> None:
    """Apply only explicit TV-01 cross-domain relations."""
    d1 = decisions[MarriageDomain.FIVE_ELEMENTS]
    d2 = decisions[MarriageDomain.STEM_BRANCH]
    d3 = decisions[MarriageDomain.TEN_GODS]
    d5 = decisions[MarriageDomain.FINANCE]
    if d1.availability.available and d2.availability.available:
        _link(d1, FindingType.SUPPORT, d2, FindingType.RISK, FindingRelation.REDUCES)
    if d3.availability.available and d5.availability.available:
        _link(d3, FindingType.RISK, d5, FindingType.RISK, FindingRelation.AMPLIFIES)
        _link(d3, FindingType.SUPPORT, d5, FindingType.SUPPORT, FindingRelation.SUPPORTS)


def _link(
    source: MarriageDomainDecision,
    source_type: FindingType,
    target: MarriageDomainDecision,
    target_type: FindingType,
    relation: FindingRelation,
) -> None:
    """Attach cross-domain refs when both sides have matching findings."""
    sources = [item for item in source.findings if item.type is source_type]
    targets = [item for item in target.findings if item.type is target_type]
    if not sources or not targets:
        return
    refs = [
        FindingReference(finding_id=item.finding_id, relation=relation)
        for item in sources
    ]
    target.cross_domain_refs.extend(refs)


def _headline_ids(findings: list[MarriageFinding]) -> list[str]:
    """Deterministic headline ids from P1 structural findings."""
    ranked = sorted(
        (item for item in findings if item.priority in {FindingPriority.P0, FindingPriority.P1}),
        key=lambda item: item.finding_id,
    )
    return [item.finding_id for item in ranked[:5]]


def _mean_confidence(items: list[MarriageEvidence]) -> float:
    """Average evidence confidence. Empty set is zero."""
    if not items:
        return 0.0
    return sum(item.confidence for item in items) / len(items)


def _overall_confidence(
    context: MarriageDecisionContext,
    tier1: list[MarriageDomainDecision],
) -> float:
    """Overall confidence from available Tier 1 domains."""
    values = [item.confidence for item in tier1 if item.availability.available]
    if values:
        return sum(values) / len(values)
    return 0.0
