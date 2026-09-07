"""Presentation placeholder. No rendering in TV1-B01."""

from __future__ import annotations

from consulting.marriage.dto.presentation import MarriagePresentationResult
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.presentation.contract import MarriagePresentationAdapter


class PlaceholderMarriagePresentationAdapter(MarriagePresentationAdapter):
    """Skeleton placeholder. Does not format or display results."""

    def adapt(self, decision: MarriageDecisionResult) -> MarriagePresentationResult:
        """Refuse presentation mapping."""
        raise NotImplementedError("TV1-B01: presentation adapter is not implemented")
