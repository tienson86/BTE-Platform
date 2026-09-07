"""Recommendation models. Action contracts derived from findings. No prose."""

from __future__ import annotations

from dataclasses import dataclass

from consulting.marriage.models.enums import FindingPriority, MarriageDomain, RecommendationType


@dataclass(slots=True)
class MarriageRecommendation:
    """One recommendation. Must reference source findings."""

    recommendation_id: str
    domain: MarriageDomain
    priority: FindingPriority
    source_finding_ids: list[str]
    action_type: RecommendationType
    narrative_key: str | None = None
    technical_reason: str | None = None
