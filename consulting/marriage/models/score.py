"""Explainable compatibility score models for TV-01."""

from __future__ import annotations

from dataclasses import dataclass, field

from consulting.marriage.models.enums import DomainGrade, MarriageDomain


@dataclass(frozen=True, slots=True)
class MarriageScoreAdjustment:
    """One bounded adjustment with a stable audit key."""

    key: str
    value: float
    detail: str | None = None


@dataclass(frozen=True, slots=True)
class MarriageDomainScoreAudit:
    """Normalized score inputs and output for one marriage domain."""

    domain: MarriageDomain
    configured_weight: float
    effective_weight: float
    score: float | None
    contribution: float
    positive_mass: float = 0.0
    negative_mass: float = 0.0
    mixed_mass: float = 0.0
    adjustments: tuple[MarriageScoreAdjustment, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    unavailable_reason: str | None = None


@dataclass(slots=True)
class MarriageScoreAudit:
    """Complete deterministic audit for the compatibility score."""

    model_version: str
    structural_score: float
    core_score: float
    overall_score: float
    grade: DomainGrade
    domain_scores: list[MarriageDomainScoreAudit] = field(default_factory=list)
    cross_domain_modifier: float = 0.0
    timing_modifier: float = 0.0
    secondary_modifier: float = 0.0
    structural_floor: float = 0.0
    structural_ceiling: float = 100.0
    modifier_audit: list[MarriageScoreAdjustment] = field(default_factory=list)

