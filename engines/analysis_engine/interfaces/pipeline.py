"""Pipeline public interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.models.analysis_context import AnalysisContext
from engines.analysis_engine.models.analysis_result import AnalysisResult
from engines.analysis_engine.models.pipeline_state import PipelineState


class PipelineInterface(ABC):
    """Public interface for Analysis Engine pipeline orchestration."""

    @abstractmethod
    def pipeline_id(self) -> str:
        """Return the stable pipeline identifier."""

    @abstractmethod
    def run(self, context: AnalysisContext) -> AnalysisResult:
        """Execute the pipeline for the provided analysis context."""

    @abstractmethod
    def state(self) -> PipelineState:
        """Return the current immutable pipeline state."""

    @abstractmethod
    def validate(self, context: AnalysisContext) -> bool:
        """Validate pipeline readiness for the provided context."""
