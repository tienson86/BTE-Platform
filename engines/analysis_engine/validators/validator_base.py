"""Analysis Engine validator base interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ValidatorBase(ABC):
    """Abstract public interface for Analysis Engine validators."""

    validator_id: str
    version: str

    def __init__(self, *, validator_id: str, version: str = "0.0.0") -> None:
        """Initialize validator identity fields."""
        self.validator_id = validator_id
        self.version = version

    @abstractmethod
    def validate(self, payload: Any) -> bool:
        """Validate a payload and return success status."""

    @abstractmethod
    def errors(self) -> tuple[str, ...]:
        """Return validation error messages from the last validation."""
