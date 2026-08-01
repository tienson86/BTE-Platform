"""Shen Sha analyzer validator skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.shensha.interfaces import ShenshaValidatorInterface
from engines.analysis_engine.analyzers.shensha.models import (
    ShenshaAnalyzerInput,
    ShenshaAnalyzerResult,
)


class ShenshaValidator(ShenshaValidatorInterface):
    """Architecture skeleton for Shen Sha analyzer validation.

    Public interface only. No validation logic.
    """

    def validate_input(self, payload: ShenshaAnalyzerInput) -> bool:
        """Validate analyzer input."""
        raise NotImplementedError

    def validate_result(self, result: ShenshaAnalyzerResult) -> bool:
        """Validate analyzer result."""
        raise NotImplementedError
