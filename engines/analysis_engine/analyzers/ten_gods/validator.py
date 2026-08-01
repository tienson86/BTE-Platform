"""Ten Gods analyzer validator skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.ten_gods.interfaces import TenGodsValidatorInterface
from engines.analysis_engine.analyzers.ten_gods.models import (
    TenGodsAnalyzerInput,
    TenGodsAnalyzerResult,
)


class TenGodsValidator(TenGodsValidatorInterface):
    """Architecture skeleton for Ten Gods analyzer validation.

    Public interface only. No validation logic.
    """

    def validate_input(self, payload: TenGodsAnalyzerInput) -> bool:
        """Validate analyzer input."""
        raise NotImplementedError

    def validate_result(self, result: TenGodsAnalyzerResult) -> bool:
        """Validate analyzer result."""
        raise NotImplementedError
