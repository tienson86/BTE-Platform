"""Analysis result validator interface.

No validation logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.models.analysis_result import AnalysisResult
from engines.analysis_engine.models.final_result import FinalResult
from engines.analysis_engine.models.module_result import ModuleResult
from engines.analysis_engine.models.stage_result import StageResult
from engines.analysis_engine.validation.validator_contract import ValidatorContract


class ResultValidator(ValidatorContract, ABC):
    """Public interface for validating analysis result contracts."""

    @abstractmethod
    def validate_analysis_result(self, result: AnalysisResult) -> bool:
        """Validate an analysis result instance."""

    @abstractmethod
    def validate_stage_result(self, result: StageResult) -> bool:
        """Validate a stage result instance."""

    @abstractmethod
    def validate_module_result(self, result: ModuleResult) -> bool:
        """Validate a module result instance."""

    @abstractmethod
    def validate_final_result(self, result: FinalResult) -> bool:
        """Validate a final result instance."""
