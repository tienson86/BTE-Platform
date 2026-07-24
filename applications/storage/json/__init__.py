"""JSON storage backend."""

from applications.storage.json.case_repository import JsonCaseRepository
from applications.storage.json.customer_repository import JsonCustomerRepository

__all__ = ["JsonCaseRepository", "JsonCustomerRepository"]
