"""Recommendation package."""

from __future__ import annotations

from consulting.marriage.recommendation.contract import MarriageRecommendationProvider
from consulting.marriage.recommendation.placeholder import (
    PlaceholderMarriageRecommendationProvider,
)

__all__ = [
    "MarriageRecommendationProvider",
    "PlaceholderMarriageRecommendationProvider",
]
