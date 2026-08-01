"""Interpretation context builder interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engines.interpretation_engine.models.final_analysis_input import FinalAnalysisInput
    from engines.interpretation_engine.models.interpretation_context_model import (
        InterpretationContextModel,
    )


class InterpretationContextBuilderInterface(ABC):
    """Build interpretation context from Pack 02 final analysis input only."""

    @abstractmethod
    def build(self, final_input: FinalAnalysisInput) -> InterpretationContextModel:
        """Build an immutable interpretation context."""

    @abstractmethod
    def validate(self, final_input: FinalAnalysisInput) -> bool:
        """Validate input before context construction."""
