"""Executable marriage.policy.v1. Domain structure and priority only. No scores."""

from __future__ import annotations

from dataclasses import dataclass

from consulting.marriage.models.enums import MarriageDomain, MarriageEvidenceType
from consulting.marriage.policy.versions import POLICY_ID, POLICY_VERSION


@dataclass(frozen=True, slots=True)
class DomainPolicy:
    """One domain inside marriage.policy.v1."""

    domain: MarriageDomain
    tier: int
    primary_types: tuple[MarriageEvidenceType, ...]
    secondary_types: tuple[MarriageEvidenceType, ...] = ()


@dataclass(frozen=True, slots=True)
class MarriagePolicyV1:
    """Canonical TV-01 Marriage Decision Policy."""

    policy_id: str
    version: str
    objectives: tuple[str, ...]
    domains: tuple[DomainPolicy, ...]


_TIER1_D1 = (
    MarriageEvidenceType.USEFUL_GOD_SUPPORT,
    MarriageEvidenceType.ELEMENT_SUPPORT,
    MarriageEvidenceType.UNFAVORABLE_ACTIVATION,
    MarriageEvidenceType.ELEMENT_CONFLICT,
)

_TIER1_D2 = (
    MarriageEvidenceType.STEM_COMBINATION,
    MarriageEvidenceType.STEM_CONTROL,
    MarriageEvidenceType.BRANCH_COMBINATION,
    MarriageEvidenceType.BRANCH_CLASH,
    MarriageEvidenceType.BRANCH_HARM,
    MarriageEvidenceType.BRANCH_PUNISHMENT,
    MarriageEvidenceType.BRANCH_BREAK,
    MarriageEvidenceType.BRANCH_MEETING,
)

_TIER1_D3 = (
    MarriageEvidenceType.TEN_GOD_SUPPORT,
    MarriageEvidenceType.TEN_GOD_PRESSURE,
    MarriageEvidenceType.ROLE_COMPLEMENT,
    MarriageEvidenceType.ROLE_CONFLICT,
)

_SECONDARY = (
    MarriageEvidenceType.SHEN_SHA_SUPPORT,
    MarriageEvidenceType.SHEN_SHA_RISK,
    MarriageEvidenceType.FENG_SHUI_REFERENCE,
)


def load_marriage_policy_v1() -> MarriagePolicyV1:
    """Return the frozen marriage.policy.v1 definition."""
    return MarriagePolicyV1(
        policy_id=POLICY_ID,
        version=POLICY_VERSION,
        objectives=(
            "relationship_stability",
            "family_harmony",
            "mutual_growth",
        ),
        domains=(
            DomainPolicy(MarriageDomain.FIVE_ELEMENTS, 1, _TIER1_D1, _SECONDARY),
            DomainPolicy(MarriageDomain.STEM_BRANCH, 1, _TIER1_D2, _SECONDARY),
            DomainPolicy(MarriageDomain.TEN_GODS, 1, _TIER1_D3, _SECONDARY),
            DomainPolicy(
                MarriageDomain.INTERACTION,
                2,
                (
                    MarriageEvidenceType.ROLE_COMPLEMENT,
                    MarriageEvidenceType.ROLE_CONFLICT,
                ),
                _SECONDARY,
            ),
            DomainPolicy(
                MarriageDomain.FINANCE,
                2,
                (
                    MarriageEvidenceType.ROLE_COMPLEMENT,
                    MarriageEvidenceType.ROLE_CONFLICT,
                    MarriageEvidenceType.TEN_GOD_SUPPORT,
                    MarriageEvidenceType.TEN_GOD_PRESSURE,
                ),
                _SECONDARY,
            ),
            DomainPolicy(MarriageDomain.FAMILY, 2, (), _SECONDARY),
            DomainPolicy(MarriageDomain.CHILDREN, 2, (), _SECONDARY),
            DomainPolicy(
                MarriageDomain.LUCK,
                3,
                (
                    MarriageEvidenceType.LUCK_ALIGNMENT,
                    MarriageEvidenceType.LUCK_MISALIGNMENT,
                ),
                _SECONDARY,
            ),
        ),
    )


def domain_policy(policy: MarriagePolicyV1, domain: MarriageDomain) -> DomainPolicy:
    """Return the policy row for a domain."""
    for item in policy.domains:
        if item.domain is domain:
            return item
    raise KeyError(domain.value)


def is_secondary_type(evidence_type: MarriageEvidenceType) -> bool:
    """Return True when the evidence type is secondary/reference."""
    return evidence_type in _SECONDARY
