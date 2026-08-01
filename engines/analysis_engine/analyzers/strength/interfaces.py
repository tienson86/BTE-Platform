"""Strength analyzer public interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.analyzers.strength.models import (
    StrengthAnalyzerInput,
    StrengthAnalyzerResult,
)
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class StrengthAnalyzerInterface(ABC):
    """Public interface for the Strength analyzer."""

    @abstractmethod
    def analyze(self, context: PipelineContext) -> StrengthAnalyzerResult:
        """Run analysis against the pipeline context."""

    @abstractmethod
    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""


class StrengthValidatorInterface(ABC):
    """Public interface for Strength analyzer validation."""

    @abstractmethod
    def validate_input(self, payload: StrengthAnalyzerInput) -> bool:
        """Validate analyzer input."""

    @abstractmethod
    def validate_result(self, result: StrengthAnalyzerResult) -> bool:
        """Validate analyzer result."""
