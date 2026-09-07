"""Marriage orchestrator contract. No business rules."""

from __future__ import annotations

from abc import ABC, abstractmethod

from consulting.marriage.dto.request import MarriageConsultationRequest
from consulting.marriage.dto.response import MarriageRuntimeResponse


class MarriageOrchestrator(ABC):
    """Orchestrates the TV-01 pipeline. Must not contain scoring or policy rules."""

    @abstractmethod
    def run(self, request: MarriageConsultationRequest) -> MarriageRuntimeResponse:
        """Execute the marriage consulting pipeline."""
