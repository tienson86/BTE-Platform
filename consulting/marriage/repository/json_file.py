"""Durable JSON repository for marriage consultation profiles."""

from __future__ import annotations

import os
from pathlib import Path
from threading import RLock

from pydantic import TypeAdapter

from consulting.marriage.dto.history import MarriageStoredResult
from consulting.marriage.repository.memory import InMemoryMarriageRepository

_RECORDS_ADAPTER = TypeAdapter(list[MarriageStoredResult])
_DEFAULT_PATH = Path(__file__).resolve().parents[3] / "applications" / "data" / "marriage_consultations.json"


class JsonMarriageRepository(InMemoryMarriageRepository):
    """Persist the complete typed consultation graph as atomic JSON."""

    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path
        self._lock = RLock()
        self._load()

    @classmethod
    def from_environment(cls) -> "JsonMarriageRepository":
        """Create the production repository from an optional path override."""
        configured = os.getenv("BTE_MARRIAGE_DATA_PATH", "").strip()
        return cls(Path(configured).expanduser() if configured else _DEFAULT_PATH)

    def save(self, stored: MarriageStoredResult) -> None:
        """Update memory and atomically flush every retained profile."""
        with self._lock:
            previous = self._records.copy(), self._order.copy(), self._idempotency.copy()
            try:
                super().save(stored)
                self._flush()
            except Exception:
                self._records, self._order, self._idempotency = previous
                raise

    def _load(self) -> None:
        if not self.path.exists():
            return
        raw = self.path.read_bytes()
        if not raw.strip():
            return
        records = _RECORDS_ADAPTER.validate_json(raw)
        for stored in records:
            super().save(stored)

    def _flush(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        records = [self._records[item] for item in self._order]
        payload = _RECORDS_ADAPTER.dump_json(records, indent=2)
        temporary = self.path.with_suffix(f"{self.path.suffix}.tmp")
        temporary.write_bytes(payload)
        temporary.replace(self.path)
