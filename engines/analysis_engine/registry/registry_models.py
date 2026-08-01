"""Analysis Engine registry models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RegistryEntry:
    """Public contract for a single registry entry."""

    entry_id: str
    object_type: str
    name: str
    version: str = "0.0.0"
    status: str = "draft"
    metadata: dict[str, Any] = field(default_factory=dict)
    references: tuple[str, ...] = ()


@dataclass(slots=True)
class RegistrySnapshot:
    """Public contract for an immutable registry snapshot."""

    snapshot_id: str
    schema_version: str
    entries: tuple[RegistryEntry, ...] = ()


@dataclass(slots=True)
class RegistryQuerySpec:
    """Public contract for a registry query request."""

    object_type: str | None = None
    entry_id: str | None = None
    name: str | None = None
    status: str | None = None
    tags: tuple[str, ...] = ()
