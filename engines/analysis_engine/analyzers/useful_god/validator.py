"""Useful God analyzer validator skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.useful_god.interfaces import UsefulGodValidatorInterface
from engines.analysis_engine.analyzers.useful_god.models import (
    UsefulGodAnalyzerInput,
    UsefulGodAnalyzerResult,
)


class UsefulGodValidator(UsefulGodValidatorInterface):
    """Architecture skeleton for Useful God analyzer validation.

    Public interface only. No validation logic.
    """

    def validate_input(self, payload: UsefulGodAnalyzerInput) -> bool:
        """Validate analyzer input."""
        raise NotImplementedError

    def validate_result(self, result: UsefulGodAnalyzerResult) -> bool:
        """Validate analyzer result."""
        raise NotImplementedError
