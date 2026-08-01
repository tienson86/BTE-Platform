"""Liunian analyzer public interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.analyzers.liunian.models import (
    LiunianAnalyzerInput,
    LiunianAnalyzerResult,
)
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class LiunianAnalyzerInterface(ABC):
    """Public interface for the Liunian analyzer."""

    @abstractmethod
    def analyze(self, context: PipelineContext) -> LiunianAnalyzerResult:
        """Run analysis against the pipeline context."""

    @abstractmethod
    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""


class LiunianValidatorInterface(ABC):
    """Public interface for Liunian analyzer validation."""

    @abstractmethod
    def validate_input(self, payload: LiunianAnalyzerInput) -> bool:
        """Validate analyzer input."""

    @abstractmethod
    def validate_result(self, result: LiunianAnalyzerResult) -> bool:
        """Validate analyzer result."""
