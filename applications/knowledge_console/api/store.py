"""In-memory + optional file-backed store for Knowledge Console assets."""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any

from applications.knowledge_console.api.models import KnowledgeAsset

_DEFAULT_DATA_DIR = Path(__file__).resolve().parent / "data"
_LOCK = threading.RLock()


class AssetStore:
    """Thread-safe asset store with JSON snapshot persistence."""

    def __init__(self, data_dir: Path | None = None) -> None:
        self._data_dir = data_dir or _DEFAULT_DATA_DIR
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._path = self._data_dir / "assets.json"
        self._assets: dict[str, KnowledgeAsset] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            return
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        for item in raw.get("assets", []):
            asset = KnowledgeAsset.from_dict(item)
            self._assets[asset.asset_id] = asset

    def _persist(self) -> None:
        payload = {
            "assets": [asset.to_dict() for asset in self._assets.values()],
        }
        self._path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def list_assets(
        self,
        *,
        asset_type: str | None = None,
        status: str | None = None,
    ) -> list[KnowledgeAsset]:
        """List assets filtered by type/status."""
        with _LOCK:
            items = list(self._assets.values())
        if asset_type:
            items = [item for item in items if item.asset_type == asset_type]
        if status:
            items = [item for item in items if item.status == status]
        items.sort(key=lambda item: item.updated_at, reverse=True)
        return items

    def get(self, asset_id: str) -> KnowledgeAsset | None:
        """Return asset or None."""
        with _LOCK:
            asset = self._assets.get(asset_id)
            return None if asset is None else KnowledgeAsset.from_dict(asset.to_dict())

    def upsert(self, asset: KnowledgeAsset) -> KnowledgeAsset:
        """Insert or replace an asset and persist."""
        with _LOCK:
            self._assets[asset.asset_id] = asset
            self._persist()
            return KnowledgeAsset.from_dict(asset.to_dict())

    def delete(self, asset_id: str) -> bool:
        """Delete an asset if present."""
        with _LOCK:
            if asset_id not in self._assets:
                return False
            del self._assets[asset_id]
            self._persist()
            return True

    def clear(self) -> None:
        """Clear all assets (tests)."""
        with _LOCK:
            self._assets.clear()
            self._persist()

    def export_all(self) -> dict[str, Any]:
        """Export raw snapshot."""
        with _LOCK:
            return {
                "assets": [asset.to_dict() for asset in self._assets.values()],
            }


_STORE: AssetStore | None = None


def get_store() -> AssetStore:
    """Return process-wide asset store."""
    global _STORE
    if _STORE is None:
        _STORE = AssetStore()
    return _STORE


def reset_store(data_dir: Path | None = None) -> AssetStore:
    """Reset process store (tests)."""
    global _STORE
    _STORE = AssetStore(data_dir=data_dir)
    return _STORE
