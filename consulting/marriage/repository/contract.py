"""Marriage repository contract. Persistence only."""

from __future__ import annotations

from abc import ABC, abstractmethod

from consulting.marriage.dto.history import MarriageHistoryRecord, MarriageStoredResult
from consulting.marriage.models.result import MarriageDecisionResult


class MarriageRepository(ABC):
    """Stores and loads marriage consultations. No decision logic."""

    @abstractmethod
    def save(self, stored: MarriageStoredResult) -> None:
        """Persist a validated consultation payload."""

    @abstractmethod
    def get(self, consultation_id: str) -> MarriageStoredResult | None:
        """Return a stored consultation by id."""

    @abstractmethod
    def get_decision(self, consultation_id: str) -> MarriageDecisionResult | None:
        """Return the factual decision payload by id."""

    @abstractmethod
    def list_history(self) -> list[MarriageHistoryRecord]:
        """Return compact history rows."""
