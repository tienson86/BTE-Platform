"""TV-01 comparative marriage decision models. Structured facts, not prose."""

from __future__ import annotations

from dataclasses import dataclass, field

from consulting.marriage.models.enums import (
    ComparisonFactKind,
    CompatibilityLevel,
    DirectionalAssessmentState,
    DirectionalSupportState,
    EvidenceSignificance,
    MarriageDomain,
    PresenceBand,
    RelationshipSubject,
)


@dataclass(frozen=True, slots=True)
class MarriageComparisonFact:
    """One customer-safe comparison fact. IDs stay internal."""

    fact_id: str
    domain: MarriageDomain
    kind: ComparisonFactKind
    subject: RelationshipSubject
    template_key: str
    slots: dict[str, str]
    evidence_ids: tuple[str, ...]
    finding_ids: tuple[str, ...]
    significance: EvidenceSignificance
    rescued: bool = False
    residual: bool = False
    confidence: float = 0.0


@dataclass(frozen=True, slots=True)
class DirectionalAssessment:
    """One-way A→B or B→A assessment for a domain."""

    subject: RelationshipSubject
    state: DirectionalAssessmentState
    needed: tuple[str, ...] = ()
    provided: tuple[str, ...] = ()
    activated_unfavorable: tuple[str, ...] = ()
    temperature_need: str | None = None


@dataclass(slots=True)
class MarriageDomainComparison:
    """Comparative decision for one marriage domain."""

    domain: MarriageDomain
    a_to_b: DirectionalAssessment
    b_to_a: DirectionalAssessment
    mutual_state: str
    strengths: list[MarriageComparisonFact] = field(default_factory=list)
    risks: list[MarriageComparisonFact] = field(default_factory=list)
    rescue: list[MarriageComparisonFact] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    conclusion_key: str | None = None
    confidence: float = 0.0
    available: bool = False


@dataclass(slots=True)
class MarriageOverallComparison:
    """Structured answers to the overall marriage questions. No prose."""

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
    five_element_state: DirectionalSupportState
    major_harmony_fact_ids: list[str] = field(default_factory=list)
    major_conflict_fact_ids: list[str] = field(default_factory=list)
    rescue_fact_ids: list[str] = field(default_factory=list)
    explanation_keys: list[str] = field(default_factory=list)


@dataclass(slots=True)
class MarriageComparisonResult:
    """TV-01 comparative decision overlay. Parallel to frozen evidence/findings."""

    five_elements: MarriageDomainComparison
    stem_branch: MarriageDomainComparison
    ten_gods: MarriageDomainComparison
    interaction: MarriageDomainComparison
    finance: MarriageDomainComparison
    family: MarriageDomainComparison
    children: MarriageDomainComparison
    luck: MarriageDomainComparison
    overall: MarriageOverallComparison
    facts: list[MarriageComparisonFact] = field(default_factory=list)
