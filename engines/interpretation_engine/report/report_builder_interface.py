"""Report builder interface for Pack 03."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from engines.interpretation_engine.models.interpretation_result_model import (
        InterpretationResultModel,
    )


class ReportBuilderInterface(ABC):
    """Report assembly contract. Formatting only at architecture boundary."""

    @abstractmethod
    def build(self, result: InterpretationResultModel) -> Any:
        """Build a report shell from an interpretation result."""

    @abstractmethod
    def validate(self, result: InterpretationResultModel) -> bool:
        """Validate report readiness."""
