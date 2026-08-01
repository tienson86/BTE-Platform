"""Temperature analyzer validator skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.temperature.interfaces import TemperatureValidatorInterface
from engines.analysis_engine.analyzers.temperature.models import (
    TemperatureAnalyzerInput,
    TemperatureAnalyzerResult,
)


class TemperatureValidator(TemperatureValidatorInterface):
    """Architecture skeleton for Temperature analyzer validation.

    Public interface only. No validation logic.
    """

    def validate_input(self, payload: TemperatureAnalyzerInput) -> bool:
        """Validate analyzer input."""
        raise NotImplementedError

    def validate_result(self, result: TemperatureAnalyzerResult) -> bool:
        """Validate analyzer result."""
        raise NotImplementedError
