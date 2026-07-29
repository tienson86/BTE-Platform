"""Persistence interfaces package."""

from applications.storage.interfaces.case_repository import CaseRepository
from applications.storage.interfaces.customer_repository import CustomerRepository
from applications.storage.interfaces.repository import (
    CaseFilter,
    CustomerFilter,
    DocumentRepository,
    Page,
    PageResult,
    Repository,
    paginate,
)

__all__ = [
    "CaseFilter",
    "CaseRepository",
    "CustomerFilter",
    "CustomerRepository",
    "DocumentRepository",
    "Page",
    "PageResult",
    "Repository",
    "paginate",
]
