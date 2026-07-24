"""Case repository interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from applications.case_management.models import CaseModel
from applications.storage.interfaces.repository import (
    CaseFilter,
    Page,
    PageResult,
    Repository,
)


class CaseRepository(Repository[CaseModel], ABC):
    """Standard case persistence contract (WP12)."""

    @abstractmethod
    def list_by_customer(self, customer_id: str) -> list[CaseModel]:
        """List cases for one customer (newest first)."""

    @abstractmethod
    def search(
        self,
        filters: CaseFilter | None = None,
        *,
        page: Page | None = None,
    ) -> PageResult[CaseModel]:
        """Search / filter with optional pagination."""
