"""Liuyue analyzer public interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.analyzers.liuyue.models import (
    LiuyueAnalyzerInput,
    LiuyueAnalyzerResult,
)
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class LiuyueAnalyzerInterface(ABC):
    """Public interface for the Liuyue analyzer."""

    @abstractmethod
    def analyze(self, context: PipelineContext) -> LiuyueAnalyzerResult:
        """Run analysis against the pipeline context."""

    @abstractmethod
    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""


class LiuyueValidatorInterface(ABC):
    """Public interface for Liuyue analyzer validation."""

    @abstractmethod
    def validate_input(self, payload: LiuyueAnalyzerInput) -> bool:
        """Validate analyzer input."""

    @abstractmethod
    def validate_result(self, result: LiuyueAnalyzerResult) -> bool:
        """Validate analyzer result."""
