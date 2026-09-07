"""Marriage recommendation catalog. Maps findings to structured actions. No prose."""

from __future__ import annotations

from dataclasses import dataclass

from consulting.marriage.models.enums import (
    FindingPriority,
    FindingType,
    MarriageDomain,
    RecommendationPriority,
    RecommendationType,
    RecommendationUrgency,
)

_UNAVAILABLE_DOMAINS = frozenset(
    {
        MarriageDomain.INTERACTION,
        MarriageDomain.FAMILY,
        MarriageDomain.CHILDREN,
        MarriageDomain.OVERALL,
    }
)

_PRIORITY_MAP: dict[FindingPriority, RecommendationPriority] = {
    FindingPriority.P0: RecommendationPriority.CRITICAL,
    FindingPriority.P1: RecommendationPriority.HIGH,
    FindingPriority.P2: RecommendationPriority.MEDIUM,
    FindingPriority.P3: RecommendationPriority.LOW,
    FindingPriority.P4: RecommendationPriority.LOW,
    FindingPriority.P5: RecommendationPriority.REFERENCE,
}


@dataclass(frozen=True, slots=True)
class ActionSpec:
    """One catalog mapping from a finding class to a structured action."""

    action_type: RecommendationType
    objective: str
    urgency: RecommendationUrgency
    expected_outcome: str
    timing_key: str
    condition: str


def unpublished_priority(priority: FindingPriority) -> bool:
    """Return True when the finding may not publish an independent action."""
    return priority is FindingPriority.P5


def domain_may_publish(domain: MarriageDomain) -> bool:
    """Return True when B04 may publish actions for the domain."""
    return domain not in _UNAVAILABLE_DOMAINS


def action_priority_for(priority: FindingPriority) -> RecommendationPriority:
    """Derive recommendation priority from finding priority."""
    return _PRIORITY_MAP[priority]


def spec_for(domain: MarriageDomain, finding_type: FindingType) -> ActionSpec | None:
    """Return the action spec for a finding class, if one exists."""
    key = (domain, finding_type)
    return _SPECS.get(key)


def _spec(
    action_type: RecommendationType,
    objective: str,
    urgency: RecommendationUrgency,
    expected_outcome: str,
    *,
    timing_key: str = "always_applicable",
    condition: str,
) -> ActionSpec:
    """Build one catalog spec."""
    return ActionSpec(
        action_type=action_type,
        objective=objective,
        urgency=urgency,
        expected_outcome=expected_outcome,
        timing_key=timing_key,
        condition=condition,
    )


_STRUCTURAL_SUPPORT = _spec(
    RecommendationType.REINFORCE_STRENGTH,
    "reinforce_existing_complement",
    RecommendationUrgency.CONTINUOUS,
    "reinforce_complementary_structure",
    condition="when_structural_support_is_present",
)
_STRUCTURAL_PRESSURE = _spec(
    RecommendationType.REDUCE_CONFLICT,
    "manage_relational_tension",
    RecommendationUrgency.CONTINUOUS,
    "preserve_stability_during_pressure",
    condition="when_relational_pressure_is_active",
)
_ROLE = _spec(
    RecommendationType.ROLE_BALANCE,
    "align_roles_and_boundaries",
    RecommendationUrgency.CONTINUOUS,
    "align_roles_and_boundaries",
    condition="when_role_pressure_or_complement_is_active",
)
_FINANCE = _spec(
    RecommendationType.FINANCIAL_STRUCTURE,
    "reduce_financial_conflict",
    RecommendationUrgency.NEAR_TERM,
    "clarify_shared_financial_responsibility",
    condition="when_joint_financial_decision",
)
_TIMING = _spec(
    RecommendationType.TIMING_AWARENESS,
    "observe_timing_activation",
    RecommendationUrgency.EVENT_DRIVEN,
    "observe_activation_window",
    timing_key="timing_finding_activation",
    condition="when_timing_window_is_active",
)

_SPECS: dict[tuple[MarriageDomain, FindingType], ActionSpec] = {
    (MarriageDomain.FIVE_ELEMENTS, FindingType.SUPPORT): _STRUCTURAL_SUPPORT,
    (MarriageDomain.FIVE_ELEMENTS, FindingType.RISK): _STRUCTURAL_PRESSURE,
    (MarriageDomain.FIVE_ELEMENTS, FindingType.MIXED): _STRUCTURAL_PRESSURE,
    (MarriageDomain.STEM_BRANCH, FindingType.SUPPORT): _STRUCTURAL_SUPPORT,
    (MarriageDomain.STEM_BRANCH, FindingType.RISK): _STRUCTURAL_PRESSURE,
    (MarriageDomain.STEM_BRANCH, FindingType.MIXED): _STRUCTURAL_PRESSURE,
    (MarriageDomain.TEN_GODS, FindingType.SUPPORT): _ROLE,
    (MarriageDomain.TEN_GODS, FindingType.RISK): _ROLE,
    (MarriageDomain.TEN_GODS, FindingType.MIXED): _ROLE,
    (MarriageDomain.FINANCE, FindingType.SUPPORT): _FINANCE,
    (MarriageDomain.FINANCE, FindingType.RISK): _FINANCE,
    (MarriageDomain.FINANCE, FindingType.MIXED): _FINANCE,
    (MarriageDomain.LUCK, FindingType.TIMING): _TIMING,
    (MarriageDomain.LUCK, FindingType.SUPPORT): _TIMING,
    (MarriageDomain.LUCK, FindingType.RISK): _TIMING,
}
