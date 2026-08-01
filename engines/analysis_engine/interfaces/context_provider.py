"""Context provider public interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.models.analysis_context import AnalysisContext


class ContextProviderInterface(ABC):
    """Public interface for providing analysis contexts."""

    @abstractmethod
    def get_context(self, context_id: str) -> AnalysisContext:
        """Return an analysis context by identifier."""

    @abstractmethod
    def create_context(
        self,
        context_id: str,
        pipeline_id: str,
        chart_id: str | None = None,
    ) -> AnalysisContext:
        """Create a new analysis context contract."""

    @abstractmethod
    def exists(self, context_id: str) -> bool:
        """Indicate whether a context identifier exists."""
