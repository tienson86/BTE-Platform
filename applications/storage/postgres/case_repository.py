"""PostgreSQL CaseRepository skeleton (not connected yet)."""

from __future__ import annotations

from applications.case_management.models import CaseModel
from applications.storage.interfaces.case_repository import CaseRepository
from applications.storage.interfaces.repository import CaseFilter, Page, PageResult
from applications.storage.postgres.customer_repository import (
    PostgresNotConfiguredError,
)


class PostgresCaseRepository(CaseRepository):
    """WP12 skeleton — real connection deferred."""

    def __init__(self, dsn: str | None = None) -> None:
        self.dsn = dsn

    def _raise(self) -> None:
        raise PostgresNotConfiguredError(
            "PostgreSQL backend is a WP12 skeleton only. "
            "Use BTE_STORAGE_BACKEND=json|sqlite for now."
        )

    def create(self, entity: CaseModel) -> CaseModel:
        """Not implemented."""
        self._raise()
        raise AssertionError("unreachable")

    def get(self, entity_id: str) -> CaseModel | None:
        """Not implemented."""
        self._raise()
        raise AssertionError("unreachable")

    def list(self) -> list[CaseModel]:
        """Not implemented."""
        self._raise()
        raise AssertionError("unreachable")

    def update(self, entity: CaseModel) -> CaseModel:
        """Not implemented."""
        self._raise()
        raise AssertionError("unreachable")

    def delete(self, entity_id: str) -> bool:
        """Not implemented."""
        self._raise()
        raise AssertionError("unreachable")

    def list_by_customer(self, customer_id: str) -> list[CaseModel]:
        """Not implemented."""
        self._raise()
        raise AssertionError("unreachable")

    def search(
        self,
        filters: CaseFilter | None = None,
        *,
        page: Page | None = None,
    ) -> PageResult[CaseModel]:
        """Not implemented."""
        self._raise()
        raise AssertionError("unreachable")
