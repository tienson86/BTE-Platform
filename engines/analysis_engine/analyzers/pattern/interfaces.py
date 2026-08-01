"""Pattern analyzer public interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.analyzers.pattern.models import (
    PatternAnalyzerInput,
    PatternAnalyzerResult,
)
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class PatternAnalyzerInterface(ABC):
    """Public interface for the Pattern analyzer."""

    @abstractmethod
    def analyze(self, context: PipelineContext) -> PatternAnalyzerResult:
        """Run analysis against the pipeline context."""

    @abstractmethod
    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""


class PatternValidatorInterface(ABC):
    """Public interface for Pattern analyzer validation."""

    @abstractmethod
    def validate_input(self, payload: PatternAnalyzerInput) -> bool:
        """Validate analyzer input."""

    @abstractmethod
    def validate_result(self, result: PatternAnalyzerResult) -> bool:
        """Validate analyzer result."""
