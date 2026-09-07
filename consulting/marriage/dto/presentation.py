"""Presentation DTOs. Display mapping only. Must not change factual results."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class MarriageIdentityView:
    """Identity block for presentation."""

    person_a_name: str | None = None
    person_b_name: str | None = None
    person_a_gender_display: str | None = None
    person_b_gender_display: str | None = None


@dataclass(slots=True)
class MarriageHeroView:
    """Compatibility hero presentation. Values must mirror factual result."""

    score_display: str
    grade_display: str
    title: str
    summary: str
    top_strengths: list[str] = field(default_factory=list)
    top_risks: list[str] = field(default_factory=list)


@dataclass(slots=True)
class MarriageFindingView:
    """Finding presentation. Bound to a finding_id."""

    finding_id: str
    title: str
    summary: str
    domain: str | None = None


@dataclass(slots=True)
class MarriageDomainView:
    """Domain presentation. Bound to a domain decision."""

    domain: str
    title: str
    summary: str
    score_display: str | None = None
    grade_display: str | None = None
    available: bool = True


@dataclass(slots=True)
class MarriageTimingView:
    """Timing presentation. Does not rewrite natal compatibility."""

    summary: str
    periods: list[str] = field(default_factory=list)


@dataclass(slots=True)
class MarriageRecommendationView:
    """Recommendation presentation. Bound to a recommendation_id."""

    recommendation_id: str
    title: str
    summary: str
    priority: str | None = None


@dataclass(slots=True)
class MarriageConfidenceView:
    """Confidence presentation."""

    level_display: str
    summary: str | None = None
    limitations: list[str] = field(default_factory=list)


@dataclass(slots=True)
class MarriagePresentationResult:
    """L6 presentation result. Must not mutate Decision Result."""

    identity: MarriageIdentityView
    hero: MarriageHeroView
    strengths: list[MarriageFindingView]
    risks: list[MarriageFindingView]
    domains: list[MarriageDomainView]
    recommendations: list[MarriageRecommendationView]
    confidence: MarriageConfidenceView
    timing: MarriageTimingView | None = None
    disclaimer: str | None = None
