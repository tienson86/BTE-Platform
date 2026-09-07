"""In-memory MarriageRepository. Persistence only. No decision logic."""

from __future__ import annotations

from consulting.marriage.dto.history import MarriageHistoryRecord, MarriageStoredResult
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.repository.contract import MarriageRepository


class InMemoryMarriageRepository(MarriageRepository):
    """Process-local store for TV1-B06. Not a production database."""

    def __init__(self) -> None:
        self._records: dict[str, MarriageStoredResult] = {}
        self._order: list[str] = []
        self._idempotency: dict[str, str] = {}

    def save(self, stored: MarriageStoredResult) -> None:
        """Persist a validated consultation payload."""
        consultation_id = stored.history.consultation_id
        if consultation_id not in self._records:
            self._order.append(consultation_id)
        self._records[consultation_id] = stored
        if stored.idempotency_key:
            self._idempotency[stored.idempotency_key] = consultation_id

    def get(self, consultation_id: str) -> MarriageStoredResult | None:
        """Return a stored consultation by id."""
        return self._records.get(consultation_id)

    def get_decision(self, consultation_id: str) -> MarriageDecisionResult | None:
        """Return the factual decision payload by id."""
        stored = self._records.get(consultation_id)
        if stored is None:
            return None
        return stored.result

    def list_history(self) -> list[MarriageHistoryRecord]:
        """Return compact history rows in insertion order."""
        return [self._records[item].history for item in self._order]

    def get_by_idempotency_key(self, key: str) -> MarriageStoredResult | None:
        """Return the consultation bound to an idempotency key, if any."""
        consultation_id = self._idempotency.get(key)
        if consultation_id is None:
            return None
        return self._records.get(consultation_id)

    def list_history_page(
        self,
        *,
        cursor: str | None,
        limit: int,
        status: str | None = None,
        language: str | None = None,
        grade: str | None = None,
    ) -> tuple[list[MarriageHistoryRecord], str | None]:
        """Return a cursor page of history rows. Newest-first by insertion."""
        rows = list(reversed(self.list_history()))
        if status:
            rows = [item for item in rows if item.status == status]
        if language:
            rows = [item for item in rows if item.language == language]
        if grade:
            rows = [item for item in rows if item.grade is not None and item.grade.value == grade]
        start = 0
        if cursor:
            for index, item in enumerate(rows):
                if item.consultation_id == cursor:
                    start = index + 1
                    break
        page = rows[start : start + limit]
        next_cursor = page[-1].consultation_id if len(page) == limit and start + limit < len(rows) else None
        return page, next_cursor
