"""Score provider public interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.models.analysis_score import AnalysisScore


class ScoreProviderInterface(ABC):
    """Public interface for retrieving analysis scores."""

    @abstractmethod
    def get_score(self, score_id: str) -> AnalysisScore:
        """Return an analysis score by identifier."""

    @abstractmethod
    def list_scores(self, result_id: str) -> tuple[AnalysisScore, ...]:
        """Return scores associated with a result identifier."""

    @abstractmethod
    def list_by_dimension(self, dimension: str) -> tuple[AnalysisScore, ...]:
        """Return scores matching a score dimension."""
