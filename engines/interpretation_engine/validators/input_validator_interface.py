"""Input validator interface for Pack 03."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engines.interpretation_engine.models.final_analysis_input import FinalAnalysisInput


class InputValidatorInterface(ABC):
    """Validate Pack 02 FinalAnalysisResult as sole input."""

    @abstractmethod
    def validate(self, final_input: FinalAnalysisInput) -> bool:
        """Validate Pack 02 final analysis input."""

    @abstractmethod
    def errors(self) -> tuple[str, ...]:
        """Return last validation error codes."""
