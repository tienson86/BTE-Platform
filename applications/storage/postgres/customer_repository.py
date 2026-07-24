"""PostgreSQL CustomerRepository skeleton (not connected yet)."""

from __future__ import annotations

from applications.customer.models import CustomerModel
from applications.storage.interfaces.customer_repository import CustomerRepository
from applications.storage.interfaces.repository import (
    CustomerFilter,
    Page,
    PageResult,
)


class PostgresNotConfiguredError(RuntimeError):
    """Raised when PostgreSQL backend is selected but not implemented."""


class PostgresCustomerRepository(CustomerRepository):
    """WP12 skeleton — real connection deferred."""

    def __init__(self, dsn: str | None = None) -> None:
        self.dsn = dsn

    def _raise(self) -> None:
        raise PostgresNotConfiguredError(
            "PostgreSQL backend is a WP12 skeleton only. "
            "Use BTE_STORAGE_BACKEND=json|sqlite for now."
        )

    def create(self, entity: CustomerModel) -> CustomerModel:
        """Not implemented."""
        self._raise()
        raise AssertionError("unreachable")

    def get(self, entity_id: str) -> CustomerModel | None:
        """Not implemented."""
        self._raise()
        raise AssertionError("unreachable")

    def list(self) -> list[CustomerModel]:
        """Not implemented."""
        self._raise()
        raise AssertionError("unreachable")

    def update(self, entity: CustomerModel) -> CustomerModel:
        """Not implemented."""
        self._raise()
        raise AssertionError("unreachable")

    def delete(self, entity_id: str) -> bool:
        """Not implemented."""
        self._raise()
        raise AssertionError("unreachable")

    def search(
        self,
        filters: CustomerFilter | None = None,
        *,
        page: Page | None = None,
    ) -> PageResult[CustomerModel]:
        """Not implemented."""
        self._raise()
        raise AssertionError("unreachable")
