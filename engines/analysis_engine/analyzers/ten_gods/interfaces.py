"""Ten Gods analyzer public interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.analyzers.ten_gods.models import (
    TenGodsAnalyzerInput,
    TenGodsAnalyzerResult,
)
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class TenGodsAnalyzerInterface(ABC):
    """Public interface for the Ten Gods analyzer."""

    @abstractmethod
    def analyze(self, context: PipelineContext) -> TenGodsAnalyzerResult:
        """Run analysis against the pipeline context."""

    @abstractmethod
    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""


class TenGodsValidatorInterface(ABC):
    """Public interface for Ten Gods analyzer validation."""

    @abstractmethod
    def validate_input(self, payload: TenGodsAnalyzerInput) -> bool:
        """Validate analyzer input."""

    @abstractmethod
    def validate_result(self, result: TenGodsAnalyzerResult) -> bool:
        """Validate analyzer result."""
