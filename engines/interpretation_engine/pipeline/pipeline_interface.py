"""Interpretation pipeline interface contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engines.interpretation_engine.models.interpretation_context_model import (
        InterpretationContextModel,
    )
    from engines.interpretation_engine.models.interpretation_result_model import (
        InterpretationResultModel,
    )


class InterpretationPipelineInterface(ABC):
    """Pipeline orchestration contract. No interpretation content logic."""

    @abstractmethod
    def pipeline_id(self) -> str:
        """Return the stable pipeline identifier."""

    @abstractmethod
    def run(self, context: InterpretationContextModel) -> InterpretationResultModel:
        """Execute the interpretation pipeline."""

    @abstractmethod
    def validate(self, context: InterpretationContextModel) -> bool:
        """Validate pipeline readiness for the provided context."""
