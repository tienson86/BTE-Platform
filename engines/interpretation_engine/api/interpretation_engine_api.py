"""Public Interpretation Engine API facade contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engines.interpretation_engine.api.interpretation_request import InterpretationRequest
    from engines.interpretation_engine.api.interpretation_response import InterpretationResponse
    from engines.interpretation_engine.models.final_analysis_input import FinalAnalysisInput
    from engines.interpretation_engine.models.interpretation_result_model import (
        InterpretationResultModel,
    )


class InterpretationEngineAPI(ABC):
    """Public API facade contract for Pack 03 Interpretation Engine.

    Accepts Pack 02 FinalAnalysisResult only. No BaZi interpretation logic.
    """

    @abstractmethod
    def interpret(self, final_input: FinalAnalysisInput) -> InterpretationResultModel:
        """Interpret a Pack 02 final analysis input."""

    @abstractmethod
    def interpret_request(self, request: InterpretationRequest) -> InterpretationResponse:
        """Interpret via a public API request envelope."""

    @abstractmethod
    def validate_input(self, final_input: FinalAnalysisInput) -> bool:
        """Validate Pack 02 final analysis input structure."""
