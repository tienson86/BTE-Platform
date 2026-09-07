"""Recommendation models. Action contracts derived from findings. No prose."""

from __future__ import annotations

from dataclasses import dataclass, field

from consulting.marriage.models.enums import (
    FindingPriority,
    MarriageDomain,
    RecommendationPriority,
    RecommendationType,
    RecommendationUrgency,
)


@dataclass(slots=True)
class MarriageRecommendation:
    """One structured action. Must reference source findings. Not customer prose."""

    recommendation_id: str
    domain: MarriageDomain
    priority: FindingPriority
    source_finding_ids: list[str]
    action_type: RecommendationType
    narrative_key: str | None = None
    technical_reason: str | None = None
    objective: str | None = None
    action_priority: RecommendationPriority | None = None
    urgency: RecommendationUrgency | None = None
    timing_key: str | None = None
    conditions: list[str] = field(default_factory=list)
    expected_outcome: str | None = None
    source_decision_id: str | None = None
    confidence: float | None = None
    version: str | None = None
    depends_on: list[str] = field(default_factory=list)
    status: str | None = None
    policy_version: str | None = None
