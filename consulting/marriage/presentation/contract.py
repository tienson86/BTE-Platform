"""Presentation adapter contract. Format only. Must not change Decision."""

from __future__ import annotations

from abc import ABC, abstractmethod

from consulting.marriage.dto.presentation import MarriagePresentationResult
from consulting.marriage.models.result import MarriageDecisionResult


class MarriagePresentationAdapter(ABC):
    """Maps Decision Result to presentation. Must not alter scores or grades."""

    @abstractmethod
    def adapt(self, decision: MarriageDecisionResult) -> MarriagePresentationResult:
        """Build a presentation result from a factual decision."""
