"""Result provider public interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.models.analysis_result import AnalysisResult
from engines.analysis_engine.models.final_result import FinalResult
from engines.analysis_engine.models.module_result import ModuleResult
from engines.analysis_engine.models.stage_result import StageResult


class ResultProviderInterface(ABC):
    """Public interface for retrieving analysis results."""

    @abstractmethod
    def get_analysis_result(self, result_id: str) -> AnalysisResult:
        """Return an analysis result by identifier."""

    @abstractmethod
    def get_stage_result(self, result_id: str) -> StageResult:
        """Return a stage result by identifier."""

    @abstractmethod
    def get_module_result(self, result_id: str) -> ModuleResult:
        """Return a module result by identifier."""

    @abstractmethod
    def get_final_result(self, result_id: str) -> FinalResult:
        """Return a final result by identifier."""
