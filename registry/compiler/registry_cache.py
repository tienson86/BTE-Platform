"""Memory, persistent, and versioned cache for Registry Compiler."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from registry.compiler.constants import COMPILER_VERSION, DEFAULT_TIMESTAMP, SCHEMA_VERSION
from registry.compiler.io_utils import read_json, write_json

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class CacheEntry:
    """Single cache entry with optional TTL metadata."""

    key: str
    value: Any
    version: str
    created_at: float
    checksum: str = ""


@dataclass(slots=True)
class RegistryCache:
    """Multi-layer cache: memory + persistent + versioned snapshot."""

    memory: dict[str, CacheEntry] = field(default_factory=dict)
    persistent_path: Path | None = None
    version: str = COMPILER_VERSION

    def get(self, key: str) -> Any | None:
        """Return a value from memory cache if present."""
        entry = self.memory.get(key)
        return None if entry is None else entry.value

    def set(
        self,
        key: str,
        value: Any,
        *,
        checksum: str = "",
        version: str | None = None,
    ) -> None:
        """Store a value in memory cache."""
        self.memory[key] = CacheEntry(
            key=key,
            value=value,
            version=version or self.version,
            created_at=time.time(),
            checksum=checksum,
        )

    def clear_memory(self) -> None:
        """Clear in-memory cache only."""
        self.memory.clear()

    def save_persistent(self, path: Path | None = None) -> Path:
        """Persist memory cache to disk (generated artifact only)."""
        target = path or self.persistent_path
        if target is None:
            raise ValueError("persistent cache path is not configured")
        payload = {
            "artifact": "registry_cache",
            "schema_version": SCHEMA_VERSION,
            "compiler_version": self.version,
            "timestamp": DEFAULT_TIMESTAMP,
            "entry_count": len(self.memory),
            "entries": {
                key: {
                    "version": entry.version,
                    "checksum": entry.checksum,
                    "created_at": DEFAULT_TIMESTAMP,
                    "value": entry.value,
                }
                for key, entry in sorted(self.memory.items())
            },
        }
        write_json(target, payload)
        self.persistent_path = target
        logger.info("Persisted registry cache to %s", target)
        return target

    def load_persistent(self, path: Path | None = None) -> int:
        """Load persistent cache into memory. Returns entry count."""
        target = path or self.persistent_path
        if target is None or not target.is_file():
            return 0
        payload = read_json(target)
        entries = payload.get("entries", {})
        if not isinstance(entries, dict):
            return 0
        loaded = 0
        for key, item in entries.items():
            if not isinstance(item, dict):
                continue
            self.memory[key] = CacheEntry(
                key=key,
                value=item.get("value"),
                version=str(item.get("version") or self.version),
                created_at=time.time(),
                checksum=str(item.get("checksum") or ""),
            )
            loaded += 1
        self.persistent_path = target
        logger.info("Loaded %s cache entries from %s", loaded, target)
        return loaded

    def version_snapshot(self) -> dict[str, Any]:
        """Return a versioned snapshot of cache keys and checksums."""
        return {
            "compiler_version": self.version,
            "schema_version": SCHEMA_VERSION,
            "keys": sorted(self.memory.keys()),
            "checksums": {
                key: entry.checksum for key, entry in sorted(self.memory.items())
            },
        }
