"""Combination analyzer public interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.analyzers.combination.models import (
    CombinationAnalyzerInput,
    CombinationAnalyzerResult,
)
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class CombinationAnalyzerInterface(ABC):
    """Public interface for the Combination analyzer."""

    @abstractmethod
    def analyze(self, context: PipelineContext) -> CombinationAnalyzerResult:
        """Run analysis against the pipeline context."""

    @abstractmethod
    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""


class CombinationValidatorInterface(ABC):
    """Public interface for Combination analyzer validation."""

    @abstractmethod
    def validate_input(self, payload: CombinationAnalyzerInput) -> bool:
        """Validate analyzer input."""

    @abstractmethod
    def validate_result(self, result: CombinationAnalyzerResult) -> bool:
        """Validate analyzer result."""
