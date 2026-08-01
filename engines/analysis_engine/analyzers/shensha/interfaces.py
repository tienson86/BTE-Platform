"""Shen Sha analyzer public interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.analyzers.shensha.models import (
    ShenshaAnalyzerInput,
    ShenshaAnalyzerResult,
)
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class ShenshaAnalyzerInterface(ABC):
    """Public interface for the Shen Sha analyzer."""

    @abstractmethod
    def analyze(self, context: PipelineContext) -> ShenshaAnalyzerResult:
        """Run analysis against the pipeline context."""

    @abstractmethod
    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""


class ShenshaValidatorInterface(ABC):
    """Public interface for Shen Sha analyzer validation."""

    @abstractmethod
    def validate_input(self, payload: ShenshaAnalyzerInput) -> bool:
        """Validate analyzer input."""

    @abstractmethod
    def validate_result(self, result: ShenshaAnalyzerResult) -> bool:
        """Validate analyzer result."""
