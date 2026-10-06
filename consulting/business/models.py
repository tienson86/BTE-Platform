"""Saved business report snapshot; calculations remain in the shared engine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class BusinessScoreGroup:
    key: str
    title: str
    configured_weight: float
    effective_weight: float
    score: float | None
    contribution: float
    confidence: float
    scored_rows: int
    total_rows: int
    explanation: str


@dataclass(frozen=True, slots=True)
class BusinessScoreAudit:
    model_version: str
    score: float | None
    coverage: float
    confidence: float
    provisional: bool
    recommendation_key: str
    recommendation: str
    advice: str
    reasons: tuple[str, ...]
    groups: tuple[BusinessScoreGroup, ...]
    methodology: str
    disclaimer: str


@dataclass(slots=True)
class BusinessProfile:
    saved_at: str
    report_model: MarriageReportModel
    assessment_cards: list[dict[str, Any]]
    business_score: BusinessScoreAudit | None = None


# The marriage archive DTO imports BusinessProfile while loading this contract.
from consulting.marriage.models.report import MarriageReportModel
