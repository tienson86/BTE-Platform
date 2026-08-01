"""Dayun analyzer validator skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.dayun.interfaces import DayunValidatorInterface
from engines.analysis_engine.analyzers.dayun.models import (
    DayunAnalyzerInput,
    DayunAnalyzerResult,
)


class DayunValidator(DayunValidatorInterface):
    """Architecture skeleton for Dayun analyzer validation.

    Public interface only. No validation logic.
    """

    def validate_input(self, payload: DayunAnalyzerInput) -> bool:
        """Validate analyzer input."""
        raise NotImplementedError

    def validate_result(self, result: DayunAnalyzerResult) -> bool:
        """Validate analyzer result."""
        raise NotImplementedError
