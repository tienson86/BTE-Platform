"""Placeholder resolution interface. No hard-coded placeholders."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class PlaceholderEngineInterface(ABC):
    """Placeholder resolution interface. No hard-coded placeholders."""

    @abstractmethod
    def resolve(self, placeholders: tuple[str, ...], context: Any) -> Any:
        """Resolve placeholder refs."""

    @abstractmethod
    def validate(self, placeholders: tuple[str, ...]) -> Any:
        """Validate placeholder reference structure."""

