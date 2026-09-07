"""API placeholder. No HTTP routes in TV1-B01."""

from __future__ import annotations

from consulting.marriage.api.contract import MarriageApiContract
from consulting.marriage.dto.history import MarriageHistoryRecord
from consulting.marriage.dto.request import MarriageConsultationRequest
from consulting.marriage.dto.response import MarriageConsultationSummary, MarriageRuntimeResponse
from consulting.marriage.models.result import MarriageDecisionResult


class PlaceholderMarriageApi(MarriageApiContract):
    """Skeleton placeholder. Does not expose HTTP endpoints."""

    def create_consultation(
        self,
        request: MarriageConsultationRequest,
    ) -> MarriageRuntimeResponse:
        """Refuse API create. Public API belongs to TV1-B06."""
        raise NotImplementedError("TV1-B01: public API is not implemented")

    def get_consultation(self, consultation_id: str) -> MarriageDecisionResult:
        """Refuse API get. Public API belongs to TV1-B06."""
        raise NotImplementedError("TV1-B01: public API is not implemented")

    def get_summary(self, consultation_id: str) -> MarriageConsultationSummary:
        """Refuse API summary. Public API belongs to TV1-B06."""
        raise NotImplementedError("TV1-B01: public API is not implemented")

    def get_report(self, consultation_id: str) -> MarriageDecisionResult:
        """Refuse API report. Public API belongs to TV1-B06."""
        raise NotImplementedError("TV1-B01: public API is not implemented")

    def list_history(self) -> list[MarriageHistoryRecord]:
        """Refuse API history. Public API belongs to TV1-B06."""
        raise NotImplementedError("TV1-B01: public API is not implemented")
