"""Presentation-safe narrative input. No snapshots, pillars, or Canonical payload."""

from __future__ import annotations

from dataclasses import dataclass

from consulting.marriage.models.enums import (
    CanonicalGender,
    ComparisonFactKind,
    CompatibilityLevel,
    ConfidenceLevel,
    DomainDecisionState,
    FindingPriority,
    FindingType,
    MarriageDomain,
    PresenceBand,
    RecommendationPriority,
    RecommendationType,
    RecommendationUrgency,
    RelationshipSubject,
)
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.narrative.facts import render_fact, render_question


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
class ComparisonNarrativeFact:
    """Presentation-safe comparison fact. Text is already rendered."""

    fact_id: str
    domain: MarriageDomain
    kind: ComparisonFactKind
    subject: RelationshipSubject
    template_key: str
    text: str
    finding_ids: list[str]
    rescued: bool
    residual: bool


@dataclass(slots=True)
class OverallComparisonNarrative:
    """Structured overall marriage answers. Narrative only renders these keys."""

    q1_compatibility: str
    q2_mutual_support: str
    q3_asymmetry: str
    q4_conflict: str
    q5_rescue: str
    q6_long_term: str
    q7_condition: str
    support_strength: PresenceBand
    conflict_strength: PresenceBand
    rescue_strength: PresenceBand
    compatibility_level: CompatibilityLevel
    five_element_state: str
    q1_text: str
    q2_text: str
    q3_text: str
    q4_text: str
    q5_text: str
    q6_text: str
    q7_text: str


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
    comparison_facts: list[ComparisonNarrativeFact]
    overall_comparison: OverallComparisonNarrative | None


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
    person_a_label = _person_label(result.person_a.display_name, "Người A")
    person_b_label = _person_label(result.person_b.display_name, "Người B")
    comparison_facts = _comparison_facts(result, person_a_label, person_b_label)
    return NarrativeInput(
        consultation_id=result.consultation_id,
        language=language,
        audience=audience,
        created_at=result.created_at,
        overall_state=result.overall.state,
        overall_confidence=result.overall.confidence,
        confidence_level=result.confidence.level,
        limitations=list(result.limitations),
        person_a_label=person_a_label,
        person_b_label=person_b_label,
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
        comparison_facts=comparison_facts,
        overall_comparison=_overall_comparison(result, comparison_facts, person_a_label, person_b_label),
    )


def _comparison_facts(
    result: MarriageDecisionResult,
    person_a: str,
    person_b: str,
) -> list[ComparisonNarrativeFact]:
    """Copy comparison facts. Narrative does not reread Canonical snapshots."""
    comparison = result.comparison
    if comparison is None:
        return []
    items: list[ComparisonNarrativeFact] = []
    for item in comparison.facts:
        items.append(
            ComparisonNarrativeFact(
                fact_id=item.fact_id,
                domain=item.domain,
                kind=item.kind,
                subject=item.subject,
                template_key=item.template_key,
                text=render_fact(item, person_a, person_b),
                finding_ids=list(item.finding_ids),
                rescued=item.rescued,
                residual=item.residual,
            )
        )
    return items


def _overall_comparison(
    result: MarriageDecisionResult,
    facts: list[ComparisonNarrativeFact],
    _person_a: str,
    _person_b: str,
) -> OverallComparisonNarrative | None:
    """Project Q1–Q7 into presentation-safe text."""
    comparison = result.comparison
    if comparison is None:
        return None
    overall = comparison.overall
    q4_text = _fact_text(facts, overall.q4_conflict, "Chưa tách được một điểm xung then chốt.")
    q7_text = _condition_text(overall.q7_condition, facts)
    return OverallComparisonNarrative(
        q1_compatibility=overall.q1_compatibility,
        q2_mutual_support=overall.q2_mutual_support,
        q3_asymmetry=overall.q3_asymmetry,
        q4_conflict=overall.q4_conflict,
        q5_rescue=overall.q5_rescue,
        q6_long_term=overall.q6_long_term,
        q7_condition=overall.q7_condition,
        support_strength=overall.support_strength,
        conflict_strength=overall.conflict_strength,
        rescue_strength=overall.rescue_strength,
        compatibility_level=overall.compatibility_level,
        five_element_state=overall.five_element_state.value,
        q1_text=_q1_text(result.overall.state.value if result.overall.state else "insufficient"),
        q2_text=render_question(overall.q2_mutual_support, "Bổ trợ hai chiều chưa đủ rõ."),
        q3_text=render_question(overall.q3_asymmetry, "Chưa thấy lệch bổ trợ một chiều rõ."),
        q4_text=q4_text,
        q5_text=render_question(overall.q5_rescue, "Yếu tố cứu giải chưa được xác lập."),
        q6_text=render_question(overall.q6_long_term, "Khả năng đi lâu dài cần đọc kèm giới hạn dữ liệu."),
        q7_text=q7_text,
    )


def _q1_text(state: str) -> str:
    """Map frozen overall state onto a consultation compatibility sentence."""
    mapping = {
        "supportive": "Nền tảng cấu trúc đang nghiêng về tương hợp hỗ trợ.",
        "balanced": "Nền tảng tương đối cân, chưa nghiêng rõ hỗ trợ hay áp lực.",
        "mixed": "Nền tảng vừa có bổ trợ vừa có điểm căng, không gộp thành một kết luận tuyệt đối.",
        "pressured": "Nền tảng đang nghiêng về áp lực hơn hỗ trợ, cần quản lý điểm lệch.",
        "critical": "Nền tảng có áp lực then chốt; đây là mức thận trọng, không phải lời kết cục.",
        "insufficient": "Chưa đủ dữ liệu cấu trúc để kết luận mức tương hợp tổng thể.",
    }
    return mapping.get(state, mapping["insufficient"])


def _fact_text(facts: list[ComparisonNarrativeFact], template_key: str, fallback: str) -> str:
    """Use the first matching comparison sentence as the conflict answer."""
    for item in facts:
        if item.template_key == template_key and item.kind.value == "conflict":
            return item.text
    return fallback


def _condition_text(key: str, facts: list[ComparisonNarrativeFact]) -> str:
    """Name the practical condition that must be managed."""
    if key == "keep_support_habits":
        return "Cần giữ thói quen phối hợp đang phát huy ở chiều bổ trợ."
    if key == "insufficient":
        return "Cần bổ sung dữ liệu trước khi chốt điều kiện vận hành."
    for item in facts:
        if item.template_key == key:
            return f"Cần quản lý đúng điểm: {item.text}."
    return "Cần quản lý điểm căng đã nêu thay vì kết luận cả mối quan hệ."


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
