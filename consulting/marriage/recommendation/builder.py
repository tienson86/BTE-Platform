"""Recommendation builder. Reads Decision/Findings only. No Canonical recalculation."""

from __future__ import annotations

from consulting.marriage.exceptions import MarriageRecommendationError
from consulting.marriage.models.decision import MarriageDomainResults
from consulting.marriage.models.enums import FindingPriority, FindingType, MarriageDomain
from consulting.marriage.models.finding import MarriageFinding
from consulting.marriage.models.recommendation import MarriageRecommendation
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.recommendation.catalog import (
    ActionSpec,
    action_priority_for,
    domain_may_publish,
    spec_for,
    unpublished_priority,
)
from consulting.marriage.recommendation.contract import MarriageRecommendationProvider
from consulting.marriage.recommendation.graph import apply_dependencies, assert_graph
from consulting.marriage.recommendation.versions import (
    RECOMMENDATION_MODEL_VERSION,
    RECOMMENDATION_STATUS_AVAILABLE,
)

_PRIORITY_RANK = {
    FindingPriority.P5: 0,
    FindingPriority.P4: 1,
    FindingPriority.P3: 2,
    FindingPriority.P2: 3,
    FindingPriority.P1: 4,
    FindingPriority.P0: 5,
}


class CanonicalRecommendationProvider(MarriageRecommendationProvider):
    """Build structured actions from a validated Marriage Decision Result."""

    def provide(self, decision: MarriageDecisionResult) -> list[MarriageRecommendation]:
        """Create recommendations bound to source findings. Empty findings yield none."""
        if not decision.findings:
            return []
        drafts = _collect_drafts(decision)
        merged = _merge(drafts)
        assigned = _assign_ids(merged, decision)
        apply_dependencies(assigned)
        assert_graph(assigned)
        return assigned


def _collect_drafts(decision: MarriageDecisionResult) -> list[MarriageRecommendation]:
    """Map eligible findings to action drafts. P1+ without a spec fails closed."""
    drafts: list[MarriageRecommendation] = []
    for finding in decision.findings:
        if unpublished_priority(finding.priority) or finding.type is FindingType.CONDITION:
            continue
        domain_available = _domain_available(decision.domains, finding.domain)
        if not domain_available or not domain_may_publish(finding.domain):
            continue
        spec = spec_for(finding.domain, finding.type)
        if spec is None:
            if _PRIORITY_RANK[finding.priority] >= _PRIORITY_RANK[FindingPriority.P1]:
                raise MarriageRecommendationError(
                    f"unmapped_high_finding:{finding.finding_id}:{finding.domain.value}"
                )
            continue
        drafts.append(_draft_from_finding(decision, finding, spec))
    return drafts


def _draft_from_finding(
    decision: MarriageDecisionResult,
    finding: MarriageFinding,
    spec: ActionSpec,
) -> MarriageRecommendation:
    """Create one unmerged action draft from a finding and catalog spec."""
    timing_key = spec.timing_key
    if finding.type is FindingType.TIMING and finding.semantic_key == "luck_misalignment":
        timing_key = "sensitive_period"
    elif finding.type is FindingType.TIMING and finding.semantic_key == "luck_alignment":
        timing_key = "supportive_period"
    conditions = [spec.condition, *finding.conditions]
    confidence = _confidence(finding.confidence, decision.limitations)
    return MarriageRecommendation(
        recommendation_id="",
        domain=finding.domain,
        priority=finding.priority,
        source_finding_ids=[finding.finding_id],
        action_type=spec.action_type,
        technical_reason=finding.semantic_key or finding.type.value,
        objective=spec.objective,
        action_priority=action_priority_for(finding.priority),
        urgency=spec.urgency,
        timing_key=timing_key,
        conditions=list(dict.fromkeys(conditions)),
        expected_outcome=spec.expected_outcome,
        source_decision_id=decision.consultation_id,
        confidence=confidence,
        version=RECOMMENDATION_MODEL_VERSION,
        status=RECOMMENDATION_STATUS_AVAILABLE,
        policy_version=decision.versions.decision_profile_version,
    )


def _merge(drafts: list[MarriageRecommendation]) -> list[MarriageRecommendation]:
    """Merge drafts that share action type, objective, and domain."""
    groups: dict[tuple[str, str, str], MarriageRecommendation] = {}
    for draft in drafts:
        key = (draft.domain.value, draft.action_type.value, draft.objective or "")
        existing = groups.get(key)
        if existing is None:
            groups[key] = draft
            continue
        existing.source_finding_ids = sorted(
            set(existing.source_finding_ids) | set(draft.source_finding_ids)
        )
        if _PRIORITY_RANK[draft.priority] > _PRIORITY_RANK[existing.priority]:
            existing.priority = draft.priority
            existing.action_priority = draft.action_priority
        existing.confidence = min(
            existing.confidence if existing.confidence is not None else 1.0,
            draft.confidence if draft.confidence is not None else 1.0,
        )
        existing.conditions = sorted(set(existing.conditions) | set(draft.conditions))
        if draft.technical_reason and draft.technical_reason not in (existing.technical_reason or ""):
            existing.technical_reason = ",".join(
                filter(None, [existing.technical_reason, draft.technical_reason])
            )
    return sorted(groups.values(), key=_sort_key)


def _assign_ids(
    drafts: list[MarriageRecommendation],
    decision: MarriageDecisionResult,
) -> list[MarriageRecommendation]:
    """Assign stable recommendation ids after merge and sort."""
    assigned: list[MarriageRecommendation] = []
    for index, draft in enumerate(drafts, start=1):
        draft.recommendation_id = f"RC-{index:04d}"
        draft.source_decision_id = decision.consultation_id
        assigned.append(draft)
    return assigned


def _sort_key(item: MarriageRecommendation) -> tuple[str, ...]:
    """Deterministic recommendation order."""
    return (
        item.domain.value,
        item.action_type.value,
        item.objective or "",
        ",".join(sorted(item.source_finding_ids)),
    )


def _domain_available(domains: MarriageDomainResults, domain: MarriageDomain) -> bool:
    """Return True when the domain has sufficient Decision support."""
    mapping = {
        MarriageDomain.FIVE_ELEMENTS: domains.five_elements,
        MarriageDomain.STEM_BRANCH: domains.stem_branch,
        MarriageDomain.TEN_GODS: domains.ten_gods,
        MarriageDomain.INTERACTION: domains.interaction,
        MarriageDomain.FINANCE: domains.finance,
        MarriageDomain.FAMILY: domains.family,
        MarriageDomain.CHILDREN: domains.children,
        MarriageDomain.LUCK: domains.luck,
    }
    decision = mapping.get(domain)
    if decision is None:
        return False
    return decision.availability.available


def _confidence(source: float, limitations: list[str]) -> float:
    """Derive action confidence from the source chain. Never exceed source."""
    value = max(0.0, min(1.0, source))
    if "birth_time_unknown" in limitations:
        value = min(value, value * 0.9)
    return value
