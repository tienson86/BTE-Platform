"""Interpreter registry models and metadata helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.exceptions.registry_error import InterpretationRegistryError


@dataclass(frozen=True, slots=True)
class InterpreterRegistryEntry:
    """Immutable registry entry for an interpreter module.

    Describes interpreter identity and dependencies only.
    Does not hold sentence templates or generated text.
    """

    entry_id: str
    interpreter_id: str
    name: str
    version: str = "0.0.0"
    status: str = "draft"
    object_type: str = "interpreter"
    domain: str = ""
    dependencies: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate structural registry entry integrity."""
        if not self.entry_id or not self.interpreter_id or not self.name:
            return False
        if not self.version:
            return False
        return True


@dataclass(frozen=True, slots=True)
class InterpreterRegistrySnapshot:
    """Immutable snapshot of interpreter registry state."""

    snapshot_id: str
    schema_version: str
    entries: tuple[InterpreterRegistryEntry, ...] = ()


class Metadata:
    """Normalize interpreter registry metadata without business interpretation."""

    def from_entry(self, entry: InterpreterRegistryEntry) -> dict[str, Any]:
        """Return a normalized metadata dictionary for a registry entry."""
        metadata = dict(entry.metadata)
        metadata.setdefault("entry_id", entry.entry_id)
        metadata.setdefault("interpreter_id", entry.interpreter_id)
        metadata.setdefault("object_type", entry.object_type)
        metadata.setdefault("name", entry.name)
        metadata.setdefault("version", entry.version)
        metadata.setdefault("status", entry.status)
        metadata.setdefault("domain", entry.domain)
        metadata.setdefault("dependencies", list(entry.dependencies))
        return metadata

    def from_snapshot(
        self,
        snapshot: InterpreterRegistrySnapshot,
    ) -> dict[str, dict[str, Any]]:
        """Return metadata keyed by entry_id for all snapshot entries."""
        return {entry.entry_id: self.from_entry(entry) for entry in snapshot.entries}

    def from_mapping(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        """Extract metadata from a flat or nested registry mapping."""
        if "metadata" in payload and isinstance(payload["metadata"], Mapping):
            metadata = dict(payload["metadata"])
            for key in (
                "entry_id",
                "interpreter_id",
                "name",
                "version",
                "status",
                "domain",
            ):
                if key in payload and key not in metadata:
                    metadata[key] = payload[key]
            return metadata
        if "entry_id" in payload or "interpreter_id" in payload:
            return dict(payload)
        raise InterpretationRegistryError("metadata_payload_unsupported")
