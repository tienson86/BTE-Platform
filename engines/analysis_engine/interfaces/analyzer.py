"""Analyzer public interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.models.analysis_context import AnalysisContext
from engines.analysis_engine.models.module_result import ModuleResult


class AnalyzerInterface(ABC):
    """Public interface for a single Analysis Engine analyzer module."""

    @abstractmethod
    def analyzer_id(self) -> str:
        """Return the stable analyzer identifier."""

    @abstractmethod
    def supports(self, context: AnalysisContext) -> bool:
        """Indicate whether this analyzer supports the provided context."""

    @abstractmethod
    def analyze(self, context: AnalysisContext) -> ModuleResult:
        """Execute analyzer logic against the provided context."""
