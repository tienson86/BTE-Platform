"""JSON-backed CustomerRepository (WP12)."""

from __future__ import annotations

from pathlib import Path

from applications.customer.models import CustomerModel
from applications.storage.interfaces.customer_repository import CustomerRepository
from applications.storage.interfaces.repository import (
    CustomerFilter,
    Page,
    PageResult,
    paginate,
)
from applications.storage.json._filters import match_customer
from applications.storage.json_store import JsonStore


class JsonCustomerRepository(CustomerRepository):
    """Persist customers as a JSON object keyed by ``customer_id``."""

    def __init__(self, path: Path | str) -> None:
        self._store = JsonStore(path)

    def _load_all(self) -> dict[str, dict]:
        raw = self._store.load_dict()
        return {
            str(key): value
            for key, value in raw.items()
            if isinstance(value, dict)
        }

    def _save_all(self, data: dict[str, dict]) -> None:
        self._store.save(data)

    def create(self, entity: CustomerModel) -> CustomerModel:
        """Insert a customer; raise if id already exists."""
        data = self._load_all()
        if entity.customer_id in data:
            raise ValueError(f"Customer already exists: {entity.customer_id}")
        data[entity.customer_id] = entity.to_dict()
        self._save_all(data)
        return entity

    def get(self, entity_id: str) -> CustomerModel | None:
        """Fetch customer by id."""
        row = self._load_all().get(entity_id)
        return CustomerModel.from_dict(row) if row else None

    def list(self) -> list[CustomerModel]:
        """List all customers sorted by created_at descending."""
        customers = [
            CustomerModel.from_dict(row) for row in self._load_all().values()
        ]
        customers.sort(key=lambda item: item.created_at, reverse=True)
        return customers

    def update(self, entity: CustomerModel) -> CustomerModel:
        """Replace an existing customer."""
        data = self._load_all()
        if entity.customer_id not in data:
            raise KeyError(f"Customer not found: {entity.customer_id}")
        entity.touch()
        data[entity.customer_id] = entity.to_dict()
        self._save_all(data)
        return entity

    def delete(self, entity_id: str) -> bool:
        """Delete customer; return True if removed."""
        data = self._load_all()
        if entity_id not in data:
            return False
        del data[entity_id]
        self._save_all(data)
        return True

    def search(
        self,
        filters: CustomerFilter | None = None,
        *,
        page: Page | None = None,
    ) -> PageResult[CustomerModel]:
        """Search / filter with optional pagination."""
        filters = filters or CustomerFilter()
        items = [c for c in self.list() if match_customer(c, filters)]
        effective = page or Page(page=1, page_size=max(len(items), 1))
        return paginate(items, effective)
