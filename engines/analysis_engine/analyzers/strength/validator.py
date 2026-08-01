"""Strength analyzer validator skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.strength.interfaces import StrengthValidatorInterface
from engines.analysis_engine.analyzers.strength.models import (
    StrengthAnalyzerInput,
    StrengthAnalyzerResult,
)


class StrengthValidator(StrengthValidatorInterface):
    """Architecture skeleton for Strength analyzer validation.

    Public interface only. No validation logic.
    """

    def validate_input(self, payload: StrengthAnalyzerInput) -> bool:
        """Validate analyzer input."""
        raise NotImplementedError

    def validate_result(self, result: StrengthAnalyzerResult) -> bool:
        """Validate analyzer result."""
        raise NotImplementedError
