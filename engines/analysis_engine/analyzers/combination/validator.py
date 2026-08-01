"""Combination analyzer validator skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.combination.interfaces import CombinationValidatorInterface
from engines.analysis_engine.analyzers.combination.models import (
    CombinationAnalyzerInput,
    CombinationAnalyzerResult,
)


class CombinationValidator(CombinationValidatorInterface):
    """Architecture skeleton for Combination analyzer validation.

    Public interface only. No validation logic.
    """

    def validate_input(self, payload: CombinationAnalyzerInput) -> bool:
        """Validate analyzer input."""
        raise NotImplementedError

    def validate_result(self, result: CombinationAnalyzerResult) -> bool:
        """Validate analyzer result."""
        raise NotImplementedError
