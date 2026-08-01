"""Useful God analyzer public interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.analyzers.useful_god.models import (
    UsefulGodAnalyzerInput,
    UsefulGodAnalyzerResult,
)
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class UsefulGodAnalyzerInterface(ABC):
    """Public interface for the Useful God analyzer."""

    @abstractmethod
    def analyze(self, context: PipelineContext) -> UsefulGodAnalyzerResult:
        """Run analysis against the pipeline context."""

    @abstractmethod
    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""


class UsefulGodValidatorInterface(ABC):
    """Public interface for Useful God analyzer validation."""

    @abstractmethod
    def validate_input(self, payload: UsefulGodAnalyzerInput) -> bool:
        """Validate analyzer input."""

    @abstractmethod
    def validate_result(self, result: UsefulGodAnalyzerResult) -> bool:
        """Validate analyzer result."""
