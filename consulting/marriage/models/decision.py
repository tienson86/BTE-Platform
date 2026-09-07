"""Decision result models. Factual output. No customer wording."""

from __future__ import annotations

from dataclasses import dataclass, field

from consulting.marriage.models.enums import DomainDecisionState, DomainGrade, MarriageDomain
from consulting.marriage.models.finding import FindingReference, MarriageFinding


@dataclass(slots=True)
class DomainAvailability:
    """Whether a domain has enough data to decide."""

    available: bool
    reason: str | None = None
    required_fields_missing: list[str] | None = None


@dataclass(slots=True)
class MarriageDomainDecision:
    """Decision for one marriage domain."""

    domain: MarriageDomain
    availability: DomainAvailability
    confidence: float
    findings: list[MarriageFinding]
    evidence_ids: list[str]
    score: float | None = None
    grade: DomainGrade | None = None
    state: DomainDecisionState | None = None
    cross_domain_refs: list[FindingReference] = field(default_factory=list)


@dataclass(slots=True)
class MarriageDomainResults:
    """All V1 domain decisions."""

    five_elements: MarriageDomainDecision
    stem_branch: MarriageDomainDecision
    ten_gods: MarriageDomainDecision
    interaction: MarriageDomainDecision
    finance: MarriageDomainDecision
    family: MarriageDomainDecision
    children: MarriageDomainDecision
    luck: MarriageDomainDecision


@dataclass(slots=True)
class MarriageOverallDecision:
    """Overall marriage decision. Finding IDs only. No customer prose."""

    score: float | None
    grade: DomainGrade | None
    confidence: float
    headline_finding_ids: list[str]
    strength_finding_ids: list[str]
    risk_finding_ids: list[str]
    condition_finding_ids: list[str]
    domain_scores: dict[MarriageDomain, float]
    state: DomainDecisionState | None = None
