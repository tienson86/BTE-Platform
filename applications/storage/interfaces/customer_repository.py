"""Customer repository interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from applications.customer.models import CustomerModel
from applications.storage.interfaces.repository import (
    CustomerFilter,
    Page,
    PageResult,
    Repository,
)


class CustomerRepository(Repository[CustomerModel], ABC):
    """Standard customer persistence contract (WP12)."""

    @abstractmethod
    def search(
        self,
        filters: CustomerFilter | None = None,
        *,
        page: Page | None = None,
    ) -> PageResult[CustomerModel]:
        """Search / filter with optional pagination."""
