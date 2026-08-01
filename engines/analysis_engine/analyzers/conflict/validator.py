"""Conflict analyzer validator skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.conflict.interfaces import ConflictValidatorInterface
from engines.analysis_engine.analyzers.conflict.models import (
    ConflictAnalyzerInput,
    ConflictAnalyzerResult,
)


class ConflictValidator(ConflictValidatorInterface):
    """Architecture skeleton for Conflict analyzer validation.

    Public interface only. No validation logic.
    """

    def validate_input(self, payload: ConflictAnalyzerInput) -> bool:
        """Validate analyzer input."""
        raise NotImplementedError

    def validate_result(self, result: ConflictAnalyzerResult) -> bool:
        """Validate analyzer result."""
        raise NotImplementedError
