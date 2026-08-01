"""Liuyue analyzer validator skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.liuyue.interfaces import LiuyueValidatorInterface
from engines.analysis_engine.analyzers.liuyue.models import (
    LiuyueAnalyzerInput,
    LiuyueAnalyzerResult,
)


class LiuyueValidator(LiuyueValidatorInterface):
    """Architecture skeleton for Liuyue analyzer validation.

    Public interface only. No validation logic.
    """

    def validate_input(self, payload: LiuyueAnalyzerInput) -> bool:
        """Validate analyzer input."""
        raise NotImplementedError

    def validate_result(self, result: LiuyueAnalyzerResult) -> bool:
        """Validate analyzer result."""
        raise NotImplementedError
