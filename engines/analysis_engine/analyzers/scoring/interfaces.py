"""Scoring analyzer public interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.analyzers.scoring.models import (
    ScoringAnalyzerInput,
    ScoringAnalyzerResult,
)
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class ScoringAnalyzerInterface(ABC):
    """Public interface for the Scoring analyzer."""

    @abstractmethod
    def analyze(self, context: PipelineContext) -> ScoringAnalyzerResult:
        """Run analysis against the pipeline context."""

    @abstractmethod
    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""


class ScoringValidatorInterface(ABC):
    """Public interface for Scoring analyzer validation."""

    @abstractmethod
    def validate_input(self, payload: ScoringAnalyzerInput) -> bool:
        """Validate analyzer input."""

    @abstractmethod
    def validate_result(self, result: ScoringAnalyzerResult) -> bool:
        """Validate analyzer result."""
