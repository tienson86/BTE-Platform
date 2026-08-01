"""Liunian analyzer validator skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.liunian.interfaces import LiunianValidatorInterface
from engines.analysis_engine.analyzers.liunian.models import (
    LiunianAnalyzerInput,
    LiunianAnalyzerResult,
)


class LiunianValidator(LiunianValidatorInterface):
    """Architecture skeleton for Liunian analyzer validation.

    Public interface only. No validation logic.
    """

    def validate_input(self, payload: LiunianAnalyzerInput) -> bool:
        """Validate analyzer input."""
        raise NotImplementedError

    def validate_result(self, result: LiunianAnalyzerResult) -> bool:
        """Validate analyzer result."""
        raise NotImplementedError
