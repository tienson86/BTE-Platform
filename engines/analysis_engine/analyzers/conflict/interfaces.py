"""Conflict analyzer public interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.analyzers.conflict.models import (
    ConflictAnalyzerInput,
    ConflictAnalyzerResult,
)
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class ConflictAnalyzerInterface(ABC):
    """Public interface for the Conflict analyzer."""

    @abstractmethod
    def analyze(self, context: PipelineContext) -> ConflictAnalyzerResult:
        """Run analysis against the pipeline context."""

    @abstractmethod
    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""


class ConflictValidatorInterface(ABC):
    """Public interface for Conflict analyzer validation."""

    @abstractmethod
    def validate_input(self, payload: ConflictAnalyzerInput) -> bool:
        """Validate analyzer input."""

    @abstractmethod
    def validate_result(self, result: ConflictAnalyzerResult) -> bool:
        """Validate analyzer result."""
