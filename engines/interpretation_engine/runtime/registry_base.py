"""Base registry contract for Pack 03 runtimes.

Dependency injection only. No singleton globals.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from engines.interpretation_engine.exceptions.interpretation_error import (
    InterpretationArchitectureError,
)

T = TypeVar("T")


class RegistryError(InterpretationArchitectureError):
    """Raised for runtime registry contract failures."""


class BaseRegistry(Generic[T]):
    """In-memory DI registry with register/unregister/lookup/list/validate."""

    def __init__(self, *, registry_id: str) -> None:
        """Initialize an empty registry."""
        self.registry_id = registry_id
        self._entries: dict[str, T] = {}

    def register(self, entry_id: str, entry: T) -> None:
        """Register an entry by identifier."""
        if not entry_id:
            raise RegistryError("registry_entry_id_required")
        if entry is None:
            raise RegistryError("registry_entry_required")
        self._entries[entry_id] = entry

    def unregister(self, entry_id: str) -> None:
        """Remove an entry by identifier."""
        self._entries.pop(entry_id, None)

    def lookup(self, entry_id: str) -> T | None:
        """Lookup an entry by identifier."""
        return self._entries.get(entry_id)

    def list(self) -> tuple[str, ...]:
        """List registered entry identifiers in deterministic order."""
        return tuple(sorted(self._entries.keys()))

    def validate(self) -> bool:
        """Validate registry structural readiness."""
        return bool(self.registry_id) and all(bool(key) for key in self._entries)
