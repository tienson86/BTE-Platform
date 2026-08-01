"""Interpretation registry interface (read-only Pack access)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class InterpretationRegistryInterface(ABC):
    """Registry contract for Pack 03. Pack 01 remains read-only."""

    @abstractmethod
    def get(self, key: str) -> Any:
        """Resolve a registry entry by key."""

    @abstractmethod
    def list_keys(self) -> tuple[str, ...]:
        """List available registry keys."""

    @abstractmethod
    def validate(self) -> bool:
        """Validate registry readiness."""
