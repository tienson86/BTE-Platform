"""Shared repository contracts and query helpers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class Page:
    """1-based pagination request."""

    page: int = 1
    page_size: int = 20

    def __post_init__(self) -> None:
        if self.page < 1:
            self.page = 1
        if self.page_size < 1:
            self.page_size = 1
        if self.page_size > 500:
            self.page_size = 500

    @property
    def offset(self) -> int:
        """SQL/list offset."""
        return (self.page - 1) * self.page_size


@dataclass(slots=True)
class PageResult(Generic[T]):
    """Paginated result set."""

    items: list[T]
    total: int
    page: int
    page_size: int

    @property
    def pages(self) -> int:
        """Total page count."""
        if self.page_size <= 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size


@dataclass(slots=True)
class CustomerFilter:
    """Customer search / filter criteria."""

    name: str | None = None
    phone: str | None = None
    email: str | None = None
    tag: str | None = None
    created_from: str | None = None
    created_to: str | None = None


@dataclass(slots=True)
class CaseFilter:
    """Case search / filter criteria."""

    customer_id: str | None = None
    engine_version: str | None = None
    created_from: str | None = None
    created_to: str | None = None


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


def paginate(items: list[T], page: Page) -> PageResult[T]:
    """Apply in-memory pagination."""
    total = len(items)
    start = page.offset
    end = start + page.page_size
    return PageResult(
        items=items[start:end],
        total=total,
        page=page.page,
        page_size=page.page_size,
    )
