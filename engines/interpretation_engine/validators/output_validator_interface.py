"""Output validator interface for Pack 03."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engines.interpretation_engine.models.interpretation_result_model import (
        InterpretationResultModel,
    )


class OutputValidatorInterface(ABC):
    """Validate interpretation result structure."""

    @abstractmethod
    def validate(self, result: InterpretationResultModel) -> bool:
        """Validate interpretation result."""

    @abstractmethod
    def errors(self) -> tuple[str, ...]:
        """Return last validation error codes."""
