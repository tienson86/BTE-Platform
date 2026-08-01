"""Temperature analyzer public interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.analyzers.temperature.models import (
    TemperatureAnalyzerInput,
    TemperatureAnalyzerResult,
)
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class TemperatureAnalyzerInterface(ABC):
    """Public interface for the Temperature analyzer."""

    @abstractmethod
    def analyze(self, context: PipelineContext) -> TemperatureAnalyzerResult:
        """Run analysis against the pipeline context."""

    @abstractmethod
    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""


class TemperatureValidatorInterface(ABC):
    """Public interface for Temperature analyzer validation."""

    @abstractmethod
    def validate_input(self, payload: TemperatureAnalyzerInput) -> bool:
        """Validate analyzer input."""

    @abstractmethod
    def validate_result(self, result: TemperatureAnalyzerResult) -> bool:
        """Validate analyzer result."""
