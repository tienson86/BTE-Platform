"""Conflict resolver public interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.models.analysis_decision import AnalysisDecision
from engines.analysis_engine.models.analysis_result import AnalysisResult


class ConflictResolverInterface(ABC):
    """Public interface for resolving conflicts among analysis decisions."""

    @abstractmethod
    def detect(self, result: AnalysisResult) -> tuple[AnalysisDecision, ...]:
        """Detect conflicting decisions within an analysis result."""

    @abstractmethod
    def resolve(
        self,
        result: AnalysisResult,
        conflicts: tuple[AnalysisDecision, ...],
    ) -> AnalysisResult:
        """Resolve detected conflicts and return an updated analysis result."""

    @abstractmethod
    def supports(self, decision_type: str) -> bool:
        """Indicate whether this resolver supports a decision type."""
