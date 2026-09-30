"""Deterministic, explainable score projection for TV-01."""

from __future__ import annotations

from collections.abc import Iterable

from consulting.canon.du_nien import lookup
from consulting.marriage.models.decision import MarriageDomainDecision
from consulting.marriage.models.enums import (
    DomainDecisionState,
    DomainGrade,
    EvidenceDirection,
    EvidenceResolutionStatus,
    EvidenceSignificance,
    FiveElement,
    MarriageDomain,
)
from consulting.marriage.models.evidence import MarriageEvidence, ResolvedMarriageEvidence
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.models.score import (
    MarriageDomainScoreAudit,
    MarriageScoreAdjustment,
    MarriageScoreAudit,
)
from consulting.marriage.policy.v1 import domain_policy, load_marriage_policy_v1
from consulting.marriage.policy.versions import ACTIVE_SCORE_MODEL_VERSION

DOMAIN_WEIGHTS: dict[MarriageDomain, float] = {
    MarriageDomain.FIVE_ELEMENTS: 20.0,
    MarriageDomain.STEM_BRANCH: 18.0,
    MarriageDomain.TEN_GODS: 18.0,
    MarriageDomain.INTERACTION: 15.0,
    MarriageDomain.FINANCE: 10.0,
    MarriageDomain.FAMILY: 8.0,
    MarriageDomain.CHILDREN: 4.0,
    MarriageDomain.LUCK: 7.0,
}

_STATE_BASE = {
    DomainDecisionState.SUPPORTIVE: 82.0,
    DomainDecisionState.BALANCED: 65.0,
    DomainDecisionState.MIXED: 50.0,
    DomainDecisionState.PRESSURED: 35.0,
    DomainDecisionState.CRITICAL: 15.0,
}

_SIGNIFICANCE_MASS = {
    EvidenceSignificance.CRITICAL: 1.0,
    EvidenceSignificance.MAJOR: 0.8,
    EvidenceSignificance.MODERATE: 0.55,
    EvidenceSignificance.MINOR: 0.3,
}

_RESOLUTION_FACTOR = {
    EvidenceResolutionStatus.ACTIVE: 1.0,
    EvidenceResolutionStatus.DAMAGED: 0.55,
    EvidenceResolutionStatus.RESCUED: 0.4,
    EvidenceResolutionStatus.SUPPRESSED: 0.2,
    EvidenceResolutionStatus.CONFLICTING: 0.6,
}

_GENERATES = {
    FiveElement.WOOD: FiveElement.FIRE,
    FiveElement.FIRE: FiveElement.EARTH,
    FiveElement.EARTH: FiveElement.METAL,
    FiveElement.METAL: FiveElement.WATER,
    FiveElement.WATER: FiveElement.WOOD,
}

_CONTROLS = {
    FiveElement.WOOD: FiveElement.EARTH,
    FiveElement.EARTH: FiveElement.WATER,
    FiveElement.WATER: FiveElement.FIRE,
    FiveElement.FIRE: FiveElement.METAL,
    FiveElement.METAL: FiveElement.WOOD,
}

_CUNG_PHI_RELATION_MODIFIER = {
    "sinh_khi": 2.0,
    "thien_y": 1.5,
    "dien_nien": 2.0,
    "phuc_vi": 1.0,
    "hoa_hai": -1.0,
    "luc_sat": -1.5,
    "ngu_quy": -2.0,
    "tuyet_menh": -2.0,
}


def project_marriage_score(result: MarriageDecisionResult) -> MarriageScoreAudit | None:
    """Project Decision meaning onto 0-100 without changing factual evidence."""
    overlay = {item.evidence_id: item for item in result.resolved_evidence}
    decisions = _domain_decisions(result)
    audits: list[MarriageDomainScoreAudit] = []
    available_scores: dict[MarriageDomain, float] = {}

    for domain, configured_weight in DOMAIN_WEIGHTS.items():
        decision = decisions[domain]
        audit = _score_domain(result, decision, configured_weight, overlay)
        audits.append(audit)
        if audit.score is not None:
            available_scores[domain] = audit.score
            decision.score = audit.score
            decision.grade = grade_for_score(audit.score)

    structural_domains = {
        domain: score
        for domain, score in available_scores.items()
        if domain is not MarriageDomain.LUCK
    }
    if not structural_domains:
        return None
    structural_score = _weighted_average(structural_domains)
    core_scores = {
        domain: score
        for domain, score in available_scores.items()
        if domain in {
            MarriageDomain.FIVE_ELEMENTS,
            MarriageDomain.STEM_BRANCH,
            MarriageDomain.TEN_GODS,
        }
    }
    core_score = _weighted_average(core_scores) if core_scores else structural_score
    cross_modifier, cross_audit = _cross_domain_modifier(available_scores)
    timing_modifier, timing_audit = _timing_modifier(available_scores.get(MarriageDomain.LUCK))
    secondary_modifier, secondary_audit = _secondary_modifier(result)
    preliminary = structural_score + cross_modifier + timing_modifier + secondary_modifier
    floor = _clamp(core_score - 12.0)
    ceiling = _clamp(core_score + 12.0)
    overall_score = round(min(ceiling, max(floor, preliminary)), 1)
    grade = grade_for_score(overall_score)

    effective_total = sum(DOMAIN_WEIGHTS[domain] for domain in structural_domains)
    normalized_audits = [
        _with_effective_weight(item, effective_total, structural_domains)
        for item in audits
    ]
    result.overall.score = overall_score
    result.overall.grade = grade
    result.overall.domain_scores = dict(available_scores)
    audit = MarriageScoreAudit(
        model_version=ACTIVE_SCORE_MODEL_VERSION,
        structural_score=round(structural_score, 1),
        core_score=round(core_score, 1),
        overall_score=overall_score,
        grade=grade,
        domain_scores=normalized_audits,
        cross_domain_modifier=cross_modifier,
        timing_modifier=timing_modifier,
        secondary_modifier=secondary_modifier,
        structural_floor=round(floor, 1),
        structural_ceiling=round(ceiling, 1),
        modifier_audit=[*cross_audit, *timing_audit, *secondary_audit],
    )
    result.score_audit = audit
    return audit


def grade_for_score(score: float) -> DomainGrade:
    """Map the frozen 0-100 bands onto Grade A-E."""
    if score >= 81.0:
        return DomainGrade.A
    if score >= 61.0:
        return DomainGrade.B
    if score >= 41.0:
        return DomainGrade.C
    if score >= 21.0:
        return DomainGrade.D
    return DomainGrade.E


def _score_domain(
    result: MarriageDecisionResult,
    decision: MarriageDomainDecision,
    configured_weight: float,
    overlay: dict[str, ResolvedMarriageEvidence],
) -> MarriageDomainScoreAudit:
    if (
        not decision.availability.available
        or decision.state is None
        or decision.state is DomainDecisionState.INSUFFICIENT
    ):
        return MarriageDomainScoreAudit(
            domain=decision.domain,
            configured_weight=configured_weight,
            effective_weight=0.0,
            score=None,
            contribution=0.0,
            unavailable_reason=decision.availability.reason or "domain_unavailable",
        )
    policy = domain_policy(load_marriage_policy_v1(), decision.domain)
    evidence = [
        item
        for item in result.evidence
        if item.domain is decision.domain
        and item.scope != "reference"
        and item.evidence_type in policy.primary_types
    ]
    positive, negative, mixed = _evidence_mass(evidence, overlay)
    total = positive + negative + mixed
    mass_adjustment = 0.0 if total == 0.0 else 8.0 * (positive - negative) / total
    adjustments = [
        MarriageScoreAdjustment(
            key="evidence_mass_balance",
            value=round(mass_adjustment, 2),
            detail="positive-negative normalized within +/-8",
        )
    ]
    if decision.domain is MarriageDomain.STEM_BRANCH:
        adjustments.append(_day_master_adjustment(result))
    raw = _STATE_BASE[decision.state] + sum(item.value for item in adjustments)
    score = round(_clamp(raw), 1)
    return MarriageDomainScoreAudit(
        domain=decision.domain,
        configured_weight=configured_weight,
        effective_weight=0.0,
        score=score,
        contribution=0.0,
        positive_mass=round(positive, 3),
        negative_mass=round(negative, 3),
        mixed_mass=round(mixed, 3),
        adjustments=tuple(adjustments),
        evidence_ids=tuple(item.evidence_id for item in evidence),
    )


def _evidence_mass(
    evidence: Iterable[MarriageEvidence],
    overlay: dict[str, ResolvedMarriageEvidence],
) -> tuple[float, float, float]:
    positive = negative = mixed = 0.0
    for item in evidence:
        resolved = overlay.get(item.evidence_id)
        factor = _RESOLUTION_FACTOR.get(
            resolved.status if resolved else EvidenceResolutionStatus.ACTIVE,
            1.0,
        )
        mass = _SIGNIFICANCE_MASS[item.significance] * item.confidence * factor
        if item.direction is EvidenceDirection.POSITIVE:
            positive += mass
        elif item.direction is EvidenceDirection.NEGATIVE:
            negative += mass
        elif item.direction is EvidenceDirection.MIXED:
            mixed += mass
    return positive, negative, mixed


def _day_master_adjustment(result: MarriageDecisionResult) -> MarriageScoreAdjustment:
    a = result.canonical_a.day_master
    b = result.canonical_b.day_master
    opposite_polarity = a.yin_yang is not b.yin_yang
    if a.element is b.element:
        value = 2.0 if opposite_polarity else 1.0
        key = "day_master_same_element"
    elif _GENERATES[a.element] is b.element or _GENERATES[b.element] is a.element:
        value = 4.0 if opposite_polarity else 3.0
        key = "day_master_generating"
    elif _CONTROLS[a.element] is b.element or _CONTROLS[b.element] is a.element:
        value = -3.0 if opposite_polarity else -4.0
        key = "day_master_controlling"
    else:
        value = 0.0
        key = "day_master_neutral"
    return MarriageScoreAdjustment(
        key=key,
        value=value,
        detail=f"{a.stem}/{a.element.value} vs {b.stem}/{b.element.value}",
    )


def _cross_domain_modifier(
    scores: dict[MarriageDomain, float],
) -> tuple[float, list[MarriageScoreAdjustment]]:
    items: list[MarriageScoreAdjustment] = []
    five = scores.get(MarriageDomain.FIVE_ELEMENTS)
    stem = scores.get(MarriageDomain.STEM_BRANCH)
    ten = scores.get(MarriageDomain.TEN_GODS)
    interaction = scores.get(MarriageDomain.INTERACTION)
    finance = scores.get(MarriageDomain.FINANCE)
    family = scores.get(MarriageDomain.FAMILY)
    if five is not None and ten is not None and five >= 61.0 and ten >= 61.0:
        items.append(MarriageScoreAdjustment("five_elements_ten_gods_support", 4.0))
    if five is not None and stem is not None and five >= 61.0 and stem >= 61.0:
        items.append(MarriageScoreAdjustment("five_elements_stem_branch_support", 2.0))
    if stem is not None and interaction is not None and stem <= 40.0 and interaction <= 40.0:
        items.append(MarriageScoreAdjustment("stem_branch_interaction_pressure", -4.0))
    if finance is not None and family is not None and finance <= 40.0 and family <= 40.0:
        items.append(MarriageScoreAdjustment("finance_family_pressure", -4.0))
    value = max(-8.0, min(8.0, sum(item.value for item in items)))
    return value, items


def _timing_modifier(score: float | None) -> tuple[float, list[MarriageScoreAdjustment]]:
    if score is None:
        return 0.0, []
    value = round(max(-5.0, min(5.0, (score - 50.0) / 10.0)), 2)
    return value, [MarriageScoreAdjustment("luck_timing", value, "bounded to +/-5")]


def _secondary_modifier(
    result: MarriageDecisionResult,
) -> tuple[float, list[MarriageScoreAdjustment]]:
    if not any(item.rule_id == "secondary.cung_phi" for item in result.evidence):
        return 0.0, []
    feng_a = result.canonical_a.feng_shui
    feng_b = result.canonical_b.feng_shui
    if feng_a is None or feng_b is None or not feng_a.cung_phi or not feng_b.cung_phi:
        return 0.0, []
    items: list[MarriageScoreAdjustment] = []
    relation = lookup(feng_a.cung_phi, feng_b.cung_phi)
    if relation is not None:
        relation_value = _CUNG_PHI_RELATION_MODIFIER.get(relation.relationship_id, 0.0)
        items.append(
            MarriageScoreAdjustment(
                key=f"cung_phi_{relation.relationship_id}",
                value=relation_value,
                detail=relation.relationship_label,
            )
        )
    group_a = _normalize_group(feng_a.group)
    group_b = _normalize_group(feng_b.group)
    if group_a and group_b:
        same = group_a == group_b
        items.append(
            MarriageScoreAdjustment(
                key="cung_phi_same_group" if same else "cung_phi_cross_group",
                value=1.0 if same else -1.0,
                detail=f"{feng_a.group} / {feng_b.group}",
            )
        )
    value = max(-3.0, min(3.0, sum(item.value for item in items)))
    return value, items


def _normalize_group(value: str | None) -> str:
    text = (value or "").strip().lower()
    if "đông" in text or text == "dong":
        return "east"
    if "tây" in text or text == "tay":
        return "west"
    return ""


def _weighted_average(scores: dict[MarriageDomain, float]) -> float:
    weight = sum(DOMAIN_WEIGHTS[item] for item in scores)
    if weight <= 0.0:
        return 50.0
    return sum(scores[item] * DOMAIN_WEIGHTS[item] for item in scores) / weight


def _with_effective_weight(
    audit: MarriageDomainScoreAudit,
    active_weight: float,
    structural_scores: dict[MarriageDomain, float],
) -> MarriageDomainScoreAudit:
    if audit.domain not in structural_scores or audit.score is None or active_weight <= 0.0:
        return audit
    effective = audit.configured_weight / active_weight
    return MarriageDomainScoreAudit(
        domain=audit.domain,
        configured_weight=audit.configured_weight,
        effective_weight=round(effective, 4),
        score=audit.score,
        contribution=round(audit.score * effective, 2),
        positive_mass=audit.positive_mass,
        negative_mass=audit.negative_mass,
        mixed_mass=audit.mixed_mass,
        adjustments=audit.adjustments,
        evidence_ids=audit.evidence_ids,
        unavailable_reason=audit.unavailable_reason,
    )


def _domain_decisions(result: MarriageDecisionResult) -> dict[MarriageDomain, MarriageDomainDecision]:
    domains = result.domains
    return {
        MarriageDomain.FIVE_ELEMENTS: domains.five_elements,
        MarriageDomain.STEM_BRANCH: domains.stem_branch,
        MarriageDomain.TEN_GODS: domains.ten_gods,
        MarriageDomain.INTERACTION: domains.interaction,
        MarriageDomain.FINANCE: domains.finance,
        MarriageDomain.FAMILY: domains.family,
        MarriageDomain.CHILDREN: domains.children,
        MarriageDomain.LUCK: domains.luck,
    }


def _clamp(value: float) -> float:
    return max(0.0, min(100.0, value))
