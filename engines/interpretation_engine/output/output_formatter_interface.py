"""Output formatter interface for Pack 03."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class OutputFormatterInterface(ABC):
    """Output format contract. No interpretation content."""

    @abstractmethod
    def format(self, payload: Any, format_id: str) -> Any:
        """Format a payload into a target output shell."""

    @abstractmethod
    def supported_formats(self) -> tuple[str, ...]:
        """Return supported format identifiers."""
