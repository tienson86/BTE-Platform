"""JSON-backed case repository."""

from __future__ import annotations

from pathlib import Path

from applications.case_management.models import CaseModel
from applications.storage.json_store import JsonStore
from applications.storage.repository import Repository


class CaseRepository(Repository[CaseModel]):
    """Persist cases as a JSON object keyed by ``case_id``."""

    def __init__(self, path: Path | str) -> None:
        self._store = JsonStore(path)

    def _load_all(self) -> dict[str, dict]:
        raw = self._store.load_dict()
        return {str(key): value for key, value in raw.items() if isinstance(value, dict)}

    def _save_all(self, data: dict[str, dict]) -> None:
        self._store.save(data)

    def create(self, entity: CaseModel) -> CaseModel:
        """Insert a case."""
        data = self._load_all()
        if entity.case_id in data:
            raise ValueError(f"Case already exists: {entity.case_id}")
        data[entity.case_id] = entity.to_dict()
        self._save_all(data)
        return entity

    def get(self, entity_id: str) -> CaseModel | None:
        """Fetch case by id."""
        data = self._load_all()
        row = data.get(entity_id)
        return CaseModel.from_dict(row) if row else None

    def list(self) -> list[CaseModel]:
        """List all cases newest first."""
        cases = [CaseModel.from_dict(row) for row in self._load_all().values()]
        cases.sort(key=lambda item: item.created_at, reverse=True)
        return cases

    def update(self, entity: CaseModel) -> CaseModel:
        """Replace an existing case."""
        data = self._load_all()
        if entity.case_id not in data:
            raise KeyError(f"Case not found: {entity.case_id}")
        data[entity.case_id] = entity.to_dict()
        self._save_all(data)
        return entity

    def delete(self, entity_id: str) -> bool:
        """Delete case; return True if removed."""
        data = self._load_all()
        if entity_id not in data:
            return False
        del data[entity_id]
        self._save_all(data)
        return True

    def list_by_customer(self, customer_id: str) -> list[CaseModel]:
        """Cases for one customer, newest first."""
        return [case for case in self.list() if case.customer_id == customer_id]
