"""Recommendation provider contract. Recommendations come from Decision only."""

from __future__ import annotations

from abc import ABC, abstractmethod

from consulting.marriage.models.recommendation import MarriageRecommendation
from consulting.marriage.models.result import MarriageDecisionResult


class MarriageRecommendationProvider(ABC):
    """Provides recommendations from a factual decision. Must not read Birth Data."""

    @abstractmethod
    def provide(self, decision: MarriageDecisionResult) -> list[MarriageRecommendation]:
        """Create recommendations bound to source findings."""
