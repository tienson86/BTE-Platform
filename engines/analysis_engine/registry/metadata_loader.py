"""Registry metadata loader runtime service."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from engines.analysis_engine.exceptions.registry_error import RegistryError
from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistrySnapshot


class MetadataLoader:
    """Load Pack-compatible registry metadata without business interpretation.

    Metadata describes governance fields only (module, owner, status, versions).
    """

    def load_from_entry(self, entry: RegistryEntry) -> dict[str, Any]:
        """Return a normalized metadata dictionary for a registry entry."""
        metadata = dict(entry.metadata)
        metadata.setdefault("entry_id", entry.entry_id)
        metadata.setdefault("object_type", entry.object_type)
        metadata.setdefault("name", entry.name)
        metadata.setdefault("version", entry.version)
        metadata.setdefault("status", entry.status)
        return metadata

    def load_from_snapshot(
        self,
        snapshot: RegistrySnapshot,
    ) -> dict[str, dict[str, Any]]:
        """Return metadata keyed by entry_id for all snapshot entries."""
        return {
            entry.entry_id: self.load_from_entry(entry) for entry in snapshot.entries
        }

    def load_from_path(self, path: Path) -> dict[str, Any]:
        """Load metadata from a Pack-compatible JSON registry record or wrapper."""
        if not path.is_file():
            raise RegistryError(f"metadata_path_not_found:{path}")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RegistryError(f"metadata_load_failed:{path}") from exc
        return self.load_from_mapping(payload)

    def load_from_mapping(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        """Extract metadata from a Pack registry record or flat mapping."""
        if "metadata" in payload and isinstance(payload["metadata"], Mapping):
            metadata = dict(payload["metadata"])
            identity = payload.get("identity")
            if isinstance(identity, Mapping):
                if "registry_id" in identity:
                    metadata.setdefault("registry_id", identity["registry_id"])
                if "object_id" in identity:
                    metadata.setdefault("object_id", identity["object_id"])
                if "namespace" in identity:
                    metadata.setdefault("namespace", identity["namespace"])
            return metadata
        if "entry_id" in payload or "registry_id" in payload:
            return dict(payload)
        raise RegistryError("metadata_payload_unsupported")
