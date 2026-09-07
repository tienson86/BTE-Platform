"""Repository placeholder. No persistence in TV1-B01."""

from __future__ import annotations

from consulting.marriage.dto.history import MarriageHistoryRecord, MarriageStoredResult
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.repository.contract import MarriageRepository


class PlaceholderMarriageRepository(MarriageRepository):
    """Skeleton placeholder. Does not read or write storage."""

    def save(self, stored: MarriageStoredResult) -> None:
        """Refuse persistence. Persistence belongs to a later build phase."""
        raise NotImplementedError("TV1-B01: repository save is not implemented")

    def get(self, consultation_id: str) -> MarriageStoredResult | None:
        """Refuse load. Persistence belongs to a later build phase."""
        raise NotImplementedError("TV1-B01: repository get is not implemented")

    def get_decision(self, consultation_id: str) -> MarriageDecisionResult | None:
        """Refuse decision load. Persistence belongs to a later build phase."""
        raise NotImplementedError("TV1-B01: repository get_decision is not implemented")

    def list_history(self) -> list[MarriageHistoryRecord]:
        """Refuse history listing. Persistence belongs to a later build phase."""
        raise NotImplementedError("TV1-B01: repository list_history is not implemented")
