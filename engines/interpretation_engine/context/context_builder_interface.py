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
    """Build interpretation context from Pack 02 final analysis input only.

    ``build`` returns the architecture model shell.
    Runtime builders also expose ``build_context`` / ``build_from_final_result``
    returning Pack 03 ``InterpretationContext``.
    """

    @abstractmethod
    def build(self, final_input: FinalAnalysisInput) -> InterpretationContextModel:
        """Build an immutable interpretation context architecture model."""

    @abstractmethod
    def validate(self, final_input: FinalAnalysisInput) -> bool:
        """Validate input before context construction."""
