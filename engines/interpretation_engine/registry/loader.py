"""Interpreter registry loader."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from engines.interpretation_engine.exceptions.registry_error import InterpretationRegistryError
from engines.interpretation_engine.registry.metadata import (
    InterpreterRegistryEntry,
    InterpreterRegistrySnapshot,
)
from engines.interpretation_engine.registry.pack_reader import PackReaderInterface

_DEFAULT_SCHEMA_VERSION = "0.0.0-architecture"
_READ_ONLY_PACKS: frozenset[str] = frozenset({"PACK_01"})


class Loader(PackReaderInterface):
    """Read-only loader for interpreter registry descriptors.

    Loads filesystem or in-memory artifacts into registry entries/snapshots.
    Never writes Pack 01 knowledge. Never generates sentences.
    """

    def __init__(
        self,
        *,
        knowledge_root: Path | None = None,
        pack_paths: Mapping[str, Path] | None = None,
    ) -> None:
        """Initialize loader with optional pack path bindings."""
        self._knowledge_root = knowledge_root
        self._pack_paths: dict[str, Path] = dict(pack_paths or {})

    def bind_pack(self, pack_id: str, path: Path) -> None:
        """Bind a pack identifier to a read-only registry artifact path."""
        self._pack_paths[pack_id] = path

    def is_read_only(self, pack_id: str) -> bool:
        """Return whether the pack is read-only for Pack 03."""
        return pack_id in _READ_ONLY_PACKS

    def read(self, pack_id: str, resource_key: str) -> Any:
        """Read a pack resource without mutation."""
        # Pack 01 access is always read-only; this loader never writes.
        path = self._resolve_pack_path(pack_id)
        payload = self._read_json(path)
        if resource_key in {"", "registry", "snapshot"}:
            return payload
        if resource_key in payload:
            return payload[resource_key]
        raise InterpretationRegistryError(
            f"pack_resource_not_found:{pack_id}:{resource_key}"
        )

    def load_snapshot(self, path: Path) -> InterpreterRegistrySnapshot:
        """Load an interpreter registry snapshot from a filesystem path."""
        payload = self._read_json(path)
        return self._snapshot_from_payload(payload, default_snapshot_id=path.stem)

    def load_pack_registry(self, pack_id: str) -> InterpreterRegistrySnapshot:
        """Load a registry snapshot for a pack identifier (Pack 01 remains read-only)."""
        path = self._resolve_pack_path(pack_id)
        payload = self._read_json(path)
        return self._snapshot_from_payload(
            payload,
            default_snapshot_id=f"{pack_id}_interpreter_registry",
        )

    def load_entries_from_mapping(
        self,
        payload: Mapping[str, Any],
    ) -> tuple[InterpreterRegistryEntry, ...]:
        """Load interpreter registry entries from an in-memory mapping."""
        snapshot = self._snapshot_from_payload(
            payload,
            default_snapshot_id="in_memory_interpreter_registry",
        )
        return snapshot.entries

    def list_entry_ids(self, path: Path) -> tuple[str, ...]:
        """List entry identifiers available at a registry path."""
        snapshot = self.load_snapshot(path)
        return tuple(entry.entry_id for entry in snapshot.entries)

    def _resolve_pack_path(self, pack_id: str) -> Path:
        """Resolve the filesystem path for a pack registry artifact."""
        if pack_id in self._pack_paths:
            return self._pack_paths[pack_id]
        if self._knowledge_root is None:
            raise InterpretationRegistryError(f"pack_path_unbound:{pack_id}")
        candidates = (
            self._knowledge_root / "registry" / "interpreter_registry.json",
            self._knowledge_root / "interpreters" / "registry.json",
        )
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        raise InterpretationRegistryError(f"pack_registry_not_found:{pack_id}")

    def _read_json(self, path: Path) -> dict[str, Any]:
        """Read a JSON object from disk."""
        if not path.is_file():
            raise InterpretationRegistryError(f"registry_path_not_found:{path}")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise InterpretationRegistryError(f"registry_load_failed:{path}") from exc
        if not isinstance(payload, dict):
            raise InterpretationRegistryError(f"registry_payload_invalid:{path}")
        return payload

    def _snapshot_from_payload(
        self,
        payload: Mapping[str, Any],
        *,
        default_snapshot_id: str,
    ) -> InterpreterRegistrySnapshot:
        """Normalize interpreter registry JSON shapes into a snapshot."""
        schema_version = str(
            payload.get("schema_version")
            or payload.get("version")
            or _DEFAULT_SCHEMA_VERSION
        )
        snapshot_id = str(payload.get("snapshot_id") or default_snapshot_id)

        if "entries" in payload and isinstance(payload["entries"], list):
            entries = tuple(
                self._entry_from_mapping(item)
                for item in payload["entries"]
                if isinstance(item, Mapping)
            )
            return InterpreterRegistrySnapshot(
                snapshot_id=snapshot_id,
                schema_version=schema_version,
                entries=entries,
            )

        if "interpreters" in payload and isinstance(payload["interpreters"], list):
            entries = tuple(
                self._entry_from_mapping(item)
                for item in payload["interpreters"]
                if isinstance(item, Mapping)
            )
            return InterpreterRegistrySnapshot(
                snapshot_id=snapshot_id,
                schema_version=schema_version,
                entries=entries,
            )

        raise InterpretationRegistryError("registry_payload_unsupported")

    def _entry_from_mapping(self, item: Mapping[str, Any]) -> InterpreterRegistryEntry:
        """Build an interpreter registry entry from a flat mapping."""
        entry_id = str(
            item.get("entry_id")
            or item.get("interpreter_id")
            or item.get("id")
            or ""
        )
        if not entry_id:
            raise InterpretationRegistryError("registry_entry_missing_id")
        interpreter_id = str(item.get("interpreter_id") or entry_id)
        name = str(item.get("name") or item.get("title") or interpreter_id)
        dependencies = self._normalize_dependencies(
            item.get("dependencies") or item.get("references") or ()
        )
        metadata = dict(item.get("metadata") or {})
        for key in ("module", "owner", "path", "tags"):
            if key in item and key not in metadata:
                metadata[key] = item[key]
        return InterpreterRegistryEntry(
            entry_id=entry_id,
            interpreter_id=interpreter_id,
            name=name,
            version=str(item.get("version") or _DEFAULT_SCHEMA_VERSION),
            status=str(item.get("status") or "draft"),
            object_type=str(item.get("object_type") or "interpreter"),
            domain=str(item.get("domain") or ""),
            dependencies=dependencies,
            metadata=metadata,
        )

    def _normalize_dependencies(self, raw: Any) -> tuple[str, ...]:
        """Normalize heterogeneous dependency payloads into identifier tuples."""
        if raw is None:
            return ()
        if isinstance(raw, str):
            return (raw,)
        dependencies: list[str] = []
        if isinstance(raw, (list, tuple)):
            for item in raw:
                if isinstance(item, str):
                    dependencies.append(item)
                elif isinstance(item, Mapping):
                    ref_id = (
                        item.get("entry_id")
                        or item.get("interpreter_id")
                        or item.get("id")
                    )
                    if ref_id:
                        dependencies.append(str(ref_id))
        return tuple(dependencies)
