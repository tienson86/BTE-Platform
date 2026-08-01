"""Validator public interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from engines.analysis_engine.models.analysis_context import AnalysisContext
from engines.analysis_engine.models.analysis_result import AnalysisResult


class ValidatorInterface(ABC):
    """Public interface for Analysis Engine validation services."""

    @abstractmethod
    def validate(self, payload: Any) -> bool:
        """Validate an arbitrary payload and return success status."""

    @abstractmethod
    def validate_context(self, context: AnalysisContext) -> bool:
        """Validate an analysis context contract."""

    @abstractmethod
    def validate_result(self, result: AnalysisResult) -> bool:
        """Validate an analysis result contract."""

    @abstractmethod
    def errors(self) -> tuple[str, ...]:
        """Return validation error messages from the last validation."""
