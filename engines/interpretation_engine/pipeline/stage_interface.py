"""Interpretation pipeline stage interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class InterpretationStageInterface(ABC):
    """Single pipeline stage contract."""

    @abstractmethod
    def stage_id(self) -> str:
        """Return the stable stage identifier."""

    @abstractmethod
    def execute(self, context: Any) -> Any:
        """Execute the stage. Architecture stub only."""

    @abstractmethod
    def validate(self, context: Any) -> bool:
        """Validate stage readiness."""
