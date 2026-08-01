"""Scoring analyzer validator skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.scoring.interfaces import ScoringValidatorInterface
from engines.analysis_engine.analyzers.scoring.models import (
    ScoringAnalyzerInput,
    ScoringAnalyzerResult,
)


class ScoringValidator(ScoringValidatorInterface):
    """Architecture skeleton for Scoring analyzer validation.

    Public interface only. No validation logic.
    """

    def validate_input(self, payload: ScoringAnalyzerInput) -> bool:
        """Validate analyzer input."""
        raise NotImplementedError

    def validate_result(self, result: ScoringAnalyzerResult) -> bool:
        """Validate analyzer result."""
        raise NotImplementedError
