"""Base interpreter interface for Pack 03."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engines.interpretation_engine.models.interpretation_context_model import (
        InterpretationContextModel,
    )
    from engines.interpretation_engine.models.interpretation_section_model import (
        InterpretationSectionModel,
    )


class InterpreterInterface(ABC):
    """Base interpreter contract. No BaZi logic. No hard-coded sentences."""

    @abstractmethod
    def interpreter_id(self) -> str:
        """Return the stable interpreter identifier."""

    @abstractmethod
    def interpret(self, context: InterpretationContextModel) -> InterpretationSectionModel:
        """Produce a section model from context. Architecture stub only."""

    @abstractmethod
    def validate(self, context: InterpretationContextModel) -> bool:
        """Validate interpreter readiness for the context."""
