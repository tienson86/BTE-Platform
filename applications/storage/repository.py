"""Repository interfaces — swappable for SQLite/PostgreSQL in WP12."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    """Generic CRUD repository contract."""

    @abstractmethod
    def create(self, entity: T) -> T:
        """Insert a new entity."""

    @abstractmethod
    def get(self, entity_id: str) -> T | None:
        """Fetch by id."""

    @abstractmethod
    def list(self) -> list[T]:
        """List all entities."""

    @abstractmethod
    def update(self, entity: T) -> T:
        """Replace an existing entity."""

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Delete by id; return True if removed."""


class DocumentRepository(Repository[dict[str, Any]], ABC):
    """Dict-document repository (JSON-friendly)."""

    @abstractmethod
    def find(self, **filters: Any) -> list[dict[str, Any]]:
        """Simple equality filters on top-level fields."""
