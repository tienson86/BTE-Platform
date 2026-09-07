"""Timing models. Activation layer only. Does not rewrite natal decision."""

from __future__ import annotations

from dataclasses import dataclass, field

from consulting.marriage.models.enums import MarriageDomain, TimingStatus


@dataclass(slots=True)
class MarriageLuckWindow:
    """Inclusive luck analysis window."""

    start_year: int
    end_year: int


@dataclass(slots=True)
class MarriageTimingPeriod:
    """One timing window classification."""

    start_year: int
    end_year: int
    status: TimingStatus
    confidence: float
    evidence_ids: list[str]
    affected_domains: list[MarriageDomain]
    score: float | None = None


@dataclass(slots=True)
class MarriageTimingResult:
    """Timing analysis result for a luck window."""

    window: MarriageLuckWindow
    periods: list[MarriageTimingPeriod]
    strongest_periods: list[str] = field(default_factory=list)
    sensitive_periods: list[str] = field(default_factory=list)
