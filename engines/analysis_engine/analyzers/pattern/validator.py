"""Pattern analyzer validator skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.pattern.interfaces import PatternValidatorInterface
from engines.analysis_engine.analyzers.pattern.models import (
    PatternAnalyzerInput,
    PatternAnalyzerResult,
)


class PatternValidator(PatternValidatorInterface):
    """Architecture skeleton for Pattern analyzer validation.

    Public interface only. No validation logic.
    """

    def validate_input(self, payload: PatternAnalyzerInput) -> bool:
        """Validate analyzer input."""
        raise NotImplementedError

    def validate_result(self, result: PatternAnalyzerResult) -> bool:
        """Validate analyzer result."""
        raise NotImplementedError
