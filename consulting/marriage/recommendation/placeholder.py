"""Recommendation placeholder. No recommendation logic in TV1-B01."""

from __future__ import annotations

from consulting.marriage.models.recommendation import MarriageRecommendation
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.recommendation.contract import MarriageRecommendationProvider


class PlaceholderMarriageRecommendationProvider(MarriageRecommendationProvider):
    """Skeleton placeholder. Does not generate actions."""

    def provide(self, decision: MarriageDecisionResult) -> list[MarriageRecommendation]:
        """Refuse recommendation generation."""
        raise NotImplementedError("TV1-B01: recommendation is not implemented")
