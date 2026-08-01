"""Cache interface for Pack 03 Interpretation Engine."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class InterpretationCacheInterface(ABC):
    """In-process cache contract. Architecture only."""

    @abstractmethod
    def get(self, key: str) -> Any | None:
        """Return a cached value if present."""

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Store a value in cache."""

    @abstractmethod
    def clear(self) -> None:
        """Clear the cache."""
