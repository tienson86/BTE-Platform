"""Analysis Engine context package public interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ContextInterface(ABC):
    """Public interface for analysis context objects."""

    @abstractmethod
    def context_id(self) -> str:
        """Return the context identifier."""

    @abstractmethod
    def get(self, key: str) -> Any:
        """Return a context value by key."""

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Assign a context value by key."""


class ContextBuilderInterface(ABC):
    """Public interface for building typed context objects."""

    @abstractmethod
    def build(self, context_id: str) -> ContextInterface:
        """Build a context instance for the given identifier."""
