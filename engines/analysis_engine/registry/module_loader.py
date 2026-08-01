"""Registry module loader runtime service."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from engines.analysis_engine.exceptions.registry_error import RegistryError
from engines.analysis_engine.registry.loader_contract import RegistryLoaderContract
from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistrySnapshot

_DEFAULT_SCHEMA_VERSION = "1.0.0"
_SUPPORTED_PACKS: frozenset[str] = frozenset({"PACK_01"})


class ModuleLoader(RegistryLoaderContract):
    """Read-only loader for Pack-compatible registry modules and snapshots.

    Loads filesystem artifacts into ``RegistrySnapshot`` models.
    Never writes, updates, or deletes Pack 01 source knowledge.
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

    def supports_pack(self, pack_id: str) -> bool:
        """Indicate whether this loader supports the given pack identifier."""
        return pack_id in _SUPPORTED_PACKS or pack_id in self._pack_paths

    def load_snapshot(self, path: Path) -> RegistrySnapshot:
        """Load a Pack-compatible registry snapshot from a filesystem path."""
        payload = self._read_json(path)
        return self._snapshot_from_payload(payload, default_snapshot_id=path.stem)

    def load_pack_registry(self, pack_id: str) -> RegistrySnapshot:
        """Load a registry snapshot for a pack identifier such as PACK_01."""
        if not self.supports_pack(pack_id):
            raise RegistryError(f"unsupported_pack:{pack_id}")
        path = self._resolve_pack_path(pack_id)
        payload = self._read_json(path)
        snapshot = self._snapshot_from_payload(
            payload,
            default_snapshot_id=f"{pack_id}_registry",
        )
        return RegistrySnapshot(
            snapshot_id=snapshot.snapshot_id,
            schema_version=snapshot.schema_version,
            entries=snapshot.entries,
        )

    def list_entry_ids(self, path: Path) -> tuple[str, ...]:
        """List entry identifiers available at a Pack-compatible registry path."""
        snapshot = self.load_snapshot(path)
        return tuple(entry.entry_id for entry in snapshot.entries)

    def _resolve_pack_path(self, pack_id: str) -> Path:
        """Resolve the filesystem path for a pack registry artifact."""
        if pack_id in self._pack_paths:
            return self._pack_paths[pack_id]
        if self._knowledge_root is None:
            raise RegistryError(f"pack_path_unbound:{pack_id}")
        candidates = (
            self._knowledge_root / "package" / "pack_registry.json",
            self._knowledge_root / "registry" / "global_registry" / "registry_index.json",
        )
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        raise RegistryError(f"pack_registry_not_found:{pack_id}")

    def _read_json(self, path: Path) -> dict[str, Any]:
        """Read a JSON object from disk."""
        if not path.is_file():
            raise RegistryError(f"registry_path_not_found:{path}")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RegistryError(f"registry_load_failed:{path}") from exc
        if not isinstance(payload, dict):
            raise RegistryError(f"registry_payload_invalid:{path}")
        return payload

    def _snapshot_from_payload(
        self,
        payload: Mapping[str, Any],
        *,
        default_snapshot_id: str,
    ) -> RegistrySnapshot:
        """Normalize supported Pack registry JSON shapes into a snapshot."""
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
            return RegistrySnapshot(
                snapshot_id=snapshot_id,
                schema_version=schema_version,
                entries=entries,
            )

        if "records" in payload and isinstance(payload["records"], list):
            entries = tuple(
                self._entry_from_pack_record(item)
                for item in payload["records"]
                if isinstance(item, Mapping)
            )
            return RegistrySnapshot(
                snapshot_id=snapshot_id,
                schema_version=schema_version,
                entries=entries,
            )

        if "packs" in payload and isinstance(payload["packs"], list):
            entries = tuple(
                self._entry_from_pack_descriptor(item)
                for item in payload["packs"]
                if isinstance(item, Mapping)
            )
            return RegistrySnapshot(
                snapshot_id=snapshot_id,
                schema_version=schema_version,
                entries=entries,
            )

        raise RegistryError("registry_payload_unsupported")

    def _entry_from_mapping(self, item: Mapping[str, Any]) -> RegistryEntry:
        """Build a registry entry from a flat Pack-compatible mapping."""
        entry_id = str(
            item.get("entry_id")
            or item.get("registry_id")
            or item.get("registry_name")
            or item.get("pack_id")
            or ""
        )
        if not entry_id:
            raise RegistryError("registry_entry_missing_id")
        object_type = str(
            item.get("object_type")
            or item.get("type")
            or "registry_object"
        )
        name = str(item.get("name") or item.get("title") or entry_id)
        version = str(item.get("version") or _DEFAULT_SCHEMA_VERSION)
        status = str(item.get("status") or "draft")
        metadata = dict(item.get("metadata") or {})
        for key in ("path", "prefix", "module", "owner", "object_id"):
            if key in item and key not in metadata:
                metadata[key] = item[key]
        references = self._normalize_references(item.get("references") or ())
        return RegistryEntry(
            entry_id=entry_id,
            object_type=object_type,
            name=name,
            version=version,
            status=status,
            metadata=metadata,
            references=references,
        )

    def _entry_from_pack_record(self, item: Mapping[str, Any]) -> RegistryEntry:
        """Build a registry entry from a Pack registry_record schema object."""
        identity = item.get("identity") if isinstance(item.get("identity"), Mapping) else {}
        metadata_block = (
            item.get("metadata") if isinstance(item.get("metadata"), Mapping) else {}
        )
        object_block = item.get("object") if isinstance(item.get("object"), Mapping) else {}
        classification = (
            item.get("classification")
            if isinstance(item.get("classification"), Mapping)
            else {}
        )
        entry_id = str(identity.get("registry_id") or "")
        if not entry_id:
            raise RegistryError("registry_record_missing_registry_id")
        dependencies = item.get("dependencies") or []
        references = self._normalize_references(dependencies)
        metadata = dict(metadata_block)
        if classification:
            metadata.setdefault("tags", list(classification.get("tags") or []))
            metadata.setdefault("domain", classification.get("domain"))
            metadata.setdefault("category", classification.get("category"))
        if identity.get("object_id"):
            metadata.setdefault("object_id", identity["object_id"])
        if identity.get("namespace"):
            metadata.setdefault("namespace", identity["namespace"])
        return RegistryEntry(
            entry_id=entry_id,
            object_type=str(object_block.get("object_type") or "registry_record"),
            name=str(object_block.get("canonical_name") or entry_id),
            version=str(metadata_block.get("version") or _DEFAULT_SCHEMA_VERSION),
            status=str(metadata_block.get("status") or "draft"),
            metadata=metadata,
            references=references,
        )

    def _entry_from_pack_descriptor(self, item: Mapping[str, Any]) -> RegistryEntry:
        """Build a registry entry from a knowledge pack descriptor."""
        pack_id = str(item.get("pack_id") or "")
        if not pack_id:
            raise RegistryError("pack_descriptor_missing_pack_id")
        depends = item.get("depends_on_packs") or []
        metadata = {
            "module_id": item.get("module_id"),
            "design_path": item.get("design_path"),
            "title": item.get("title"),
        }
        return RegistryEntry(
            entry_id=pack_id,
            object_type="knowledge_pack",
            name=str(item.get("title") or pack_id),
            version=str(item.get("version") or _DEFAULT_SCHEMA_VERSION),
            status=str(item.get("status") or "draft"),
            metadata=metadata,
            references=self._normalize_references(depends),
        )

    def _normalize_references(self, raw: Any) -> tuple[str, ...]:
        """Normalize heterogeneous reference payloads into identifier tuples."""
        if raw is None:
            return ()
        if isinstance(raw, str):
            return (raw,)
        references: list[str] = []
        if isinstance(raw, (list, tuple)):
            for item in raw:
                if isinstance(item, str):
                    references.append(item)
                elif isinstance(item, Mapping):
                    ref_id = (
                        item.get("registry_id")
                        or item.get("entry_id")
                        or item.get("object_id")
                        or item.get("pack_id")
                    )
                    if ref_id:
                        references.append(str(ref_id))
        return tuple(references)
