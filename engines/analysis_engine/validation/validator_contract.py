"""Core validator contract interface.

No validation logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ValidatorContract(ABC):
    """Public contract for Analysis Engine validators."""

    @abstractmethod
    def validator_id(self) -> str:
        """Return the stable validator identifier."""

    @abstractmethod
    def validate(self, payload: Any) -> bool:
        """Validate a payload and return success status."""

    @abstractmethod
    def errors(self) -> tuple[str, ...]:
        """Return validation error messages from the last validation."""
