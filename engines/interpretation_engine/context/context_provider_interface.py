"""Interpretation context provider interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engines.interpretation_engine.models.interpretation_context_model import (
        InterpretationContextModel,
    )


class InterpretationContextProviderInterface(ABC):
    """Provide access to an active interpretation context."""

    @abstractmethod
    def get(self, context_id: str) -> InterpretationContextModel:
        """Return a context by id."""

    @abstractmethod
    def current(self) -> InterpretationContextModel | None:
        """Return the current context if any."""
