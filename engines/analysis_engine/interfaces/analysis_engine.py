"""Analysis Engine top-level public interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.models.analysis_context import AnalysisContext
from engines.analysis_engine.models.analysis_result import AnalysisResult
from engines.analysis_engine.models.final_result import FinalResult


class AnalysisEngineInterface(ABC):
    """Public interface for the Analysis Engine orchestration boundary."""

    @abstractmethod
    def analyze(self, context: AnalysisContext) -> AnalysisResult:
        """Run analysis for the provided context and return an analysis result."""

    @abstractmethod
    def finalize(self, result: AnalysisResult) -> FinalResult:
        """Finalize an analysis result into a final aggregated result."""

    @abstractmethod
    def validate_context(self, context: AnalysisContext) -> bool:
        """Validate that an analysis context is acceptable for execution."""
