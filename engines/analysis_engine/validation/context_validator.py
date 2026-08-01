"""Analysis context validator interface.

No validation logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.models.analysis_context import AnalysisContext
from engines.analysis_engine.validation.validator_contract import ValidatorContract


class ContextValidator(ValidatorContract, ABC):
    """Public interface for validating analysis context contracts."""

    @abstractmethod
    def validate_context(self, context: AnalysisContext) -> bool:
        """Validate an analysis context instance."""

    @abstractmethod
    def validate_required_fields(self, context: AnalysisContext) -> bool:
        """Validate required context fields are present."""
