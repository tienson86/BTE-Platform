"""Analysis score validator interface.

No validation logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.models.analysis_score import AnalysisScore
from engines.analysis_engine.validation.validator_contract import ValidatorContract


class ScoreValidator(ValidatorContract, ABC):
    """Public interface for validating analysis score contracts."""

    @abstractmethod
    def validate_score(self, score: AnalysisScore) -> bool:
        """Validate an analysis score instance."""

    @abstractmethod
    def validate_score_set(self, scores: tuple[AnalysisScore, ...]) -> bool:
        """Validate a set of analysis scores."""

    @abstractmethod
    def validate_dimension(self, dimension: str) -> bool:
        """Validate a score dimension identifier."""
