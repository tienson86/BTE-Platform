"""Presentation-safe narrative input. No snapshots, pillars, or Canonical payload."""

from __future__ import annotations

from dataclasses import dataclass

from consulting.marriage.models.enums import (
    CanonicalGender,
    ConfidenceLevel,
    DomainDecisionState,
    FindingPriority,
    FindingType,
    MarriageDomain,
    RecommendationPriority,
    RecommendationType,
    RecommendationUrgency,
)
from consulting.marriage.models.result import MarriageDecisionResult


@dataclass(slots=True)
class FindingNarrativeInput:
    """Finding facts Narrative may explain. Not a new finding."""

    finding_id: str
    domain: MarriageDomain
    finding_type: FindingType
    priority: FindingPriority
    semantic_key: str | None
    confidence: float
    conditions: list[str]


@dataclass(slots=True)
class DomainNarrativeInput:
    """Domain decision facts Narrative may explain."""

    domain: MarriageDomain
    available: bool
    state: DomainDecisionState | None
    confidence: float
    finding_ids: list[str]
    unavailable_reason: str | None


@dataclass(slots=True)
class RecommendationNarrativeInput:
    """Structured action facts Narrative may communicate. Not a new action."""

    recommendation_id: str
    domain: MarriageDomain
    action_type: RecommendationType
    objective: str | None
    action_priority: RecommendationPriority | None
    urgency: RecommendationUrgency | None
    timing_key: str | None
    expected_outcome: str | None
    source_finding_ids: list[str]
    conditions: list[str]
    confidence: float | None


@dataclass(slots=True)
class NarrativeInput:
    """Allowed Narrative boundary. Built from Decision and Recommendation only."""

    consultation_id: str
    language: str
    audience: str
    created_at: str
    overall_state: DomainDecisionState
    overall_confidence: float
    confidence_level: ConfidenceLevel
    limitations: list[str]
    person_a_label: str
    person_b_label: str
    person_a_gender: CanonicalGender
    person_b_gender: CanonicalGender
    hour_known: bool
    strength_finding_ids: list[str]
    risk_finding_ids: list[str]
    headline_finding_ids: list[str]
    domains: list[DomainNarrativeInput]
    findings: list[FindingNarrativeInput]
    recommendations: list[RecommendationNarrativeInput]
    module_version: str
    policy_version: str
    score_model_version: str
    person_a_correlation_id: str
    person_b_correlation_id: str


def narrative_input_from_decision(
    result: MarriageDecisionResult,
    *,
    language: str,
    audience: str,
) -> NarrativeInput:
    """Copy presentation-safe Decision/Recommendation facts. Do not reread Canonical."""
    if result.overall.state is None:
        raise ValueError("overall_state_required")
    findings = [
        FindingNarrativeInput(
            finding_id=item.finding_id,
            domain=item.domain,
            finding_type=item.type,
            priority=item.priority,
            semantic_key=item.semantic_key,
            confidence=item.confidence,
            conditions=list(item.conditions),
        )
        for item in result.findings
    ]
    domains = [_domain_input(item) for item in _iter_domains(result)]
    recommendations = [
        RecommendationNarrativeInput(
            recommendation_id=item.recommendation_id,
            domain=item.domain,
            action_type=item.action_type,
            objective=item.objective,
            action_priority=item.action_priority,
            urgency=item.urgency,
            timing_key=item.timing_key,
            expected_outcome=item.expected_outcome,
            source_finding_ids=list(item.source_finding_ids),
            conditions=list(item.conditions),
            confidence=item.confidence,
        )
        for item in result.recommendations
    ]
    hour_known = (
        result.person_a.birth_data_quality.birth_time_known
        and result.person_b.birth_data_quality.birth_time_known
    )
    return NarrativeInput(
        consultation_id=result.consultation_id,
        language=language,
        audience=audience,
        created_at=result.created_at,
        overall_state=result.overall.state,
        overall_confidence=result.overall.confidence,
        confidence_level=result.confidence.level,
        limitations=list(result.limitations),
        person_a_label=_person_label(result.person_a.display_name, "Người A"),
        person_b_label=_person_label(result.person_b.display_name, "Người B"),
        person_a_gender=result.person_a.gender,
        person_b_gender=result.person_b.gender,
        hour_known=hour_known,
        strength_finding_ids=list(result.overall.strength_finding_ids),
        risk_finding_ids=list(result.overall.risk_finding_ids),
        headline_finding_ids=list(result.overall.headline_finding_ids),
        domains=domains,
        findings=findings,
        recommendations=recommendations,
        module_version=result.versions.module_version,
        policy_version=result.versions.decision_profile_version,
        score_model_version=result.versions.score_model_version,
        person_a_correlation_id=result.person_a.analysis_id,
        person_b_correlation_id=result.person_b.analysis_id,
    )


def _person_label(display_name: str | None, fallback: str) -> str:
    """Use presentation-safe identity only. Do not infer from birth data."""
    if display_name and display_name.strip():
        return display_name.strip()
    return fallback


def _domain_input(decision: object) -> DomainNarrativeInput:
    """Project one domain decision onto Narrative input."""
    from consulting.marriage.models.decision import MarriageDomainDecision

    item = decision
    if not isinstance(item, MarriageDomainDecision):
        raise TypeError("domain_decision_required")
    return DomainNarrativeInput(
        domain=item.domain,
        available=item.availability.available,
        state=item.state,
        confidence=item.confidence,
        finding_ids=[finding.finding_id for finding in item.findings],
        unavailable_reason=item.availability.reason,
    )


def _iter_domains(result: MarriageDecisionResult) -> tuple[object, ...]:
    """Return domains in the frozen V1 order."""
    domains = result.domains
    return (
        domains.five_elements,
        domains.stem_branch,
        domains.ten_gods,
        domains.interaction,
        domains.finance,
        domains.family,
        domains.children,
        domains.luck,
    )
