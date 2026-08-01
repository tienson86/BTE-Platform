"""Dayun analyzer public interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.analyzers.dayun.models import (
    DayunAnalyzerInput,
    DayunAnalyzerResult,
)
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class DayunAnalyzerInterface(ABC):
    """Public interface for the Dayun analyzer."""

    @abstractmethod
    def analyze(self, context: PipelineContext) -> DayunAnalyzerResult:
        """Run analysis against the pipeline context."""

    @abstractmethod
    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""


class DayunValidatorInterface(ABC):
    """Public interface for Dayun analyzer validation."""

    @abstractmethod
    def validate_input(self, payload: DayunAnalyzerInput) -> bool:
        """Validate analyzer input."""

    @abstractmethod
    def validate_result(self, result: DayunAnalyzerResult) -> bool:
        """Validate analyzer result."""
