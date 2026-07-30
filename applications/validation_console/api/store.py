"""Thread-safe JSON store for Validation Console datasets."""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any

from applications.validation_console.api.models import GoldenDataset

_DEFAULT_DATA_DIR = Path(__file__).resolve().parent / "data"
_LOCK = threading.RLock()


class DatasetStore:
    """Persist managed golden datasets (workspace only)."""

    def __init__(self, data_dir: Path | None = None) -> None:
        self._data_dir = data_dir or _DEFAULT_DATA_DIR
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._path = self._data_dir / "datasets.json"
        self._datasets: dict[str, GoldenDataset] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            return
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        for item in raw.get("datasets", []):
            dataset = GoldenDataset.from_dict(item)
            self._datasets[dataset.dataset_id] = dataset

    def _persist(self) -> None:
        payload = {
            "datasets": [item.to_dict() for item in self._datasets.values()],
        }
        self._path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def list_datasets(
        self,
        *,
        status: str | None = None,
        module: str | None = None,
    ) -> list[GoldenDataset]:
        """List datasets with optional filters."""
        with _LOCK:
            items = list(self._datasets.values())
        if status:
            items = [item for item in items if item.status == status]
        if module:
            items = [item for item in items if item.module == module]
        items.sort(key=lambda item: item.updated_at, reverse=True)
        return items

    def get(self, dataset_id: str) -> GoldenDataset | None:
        """Return dataset or None."""
        with _LOCK:
            dataset = self._datasets.get(dataset_id)
            return (
                None
                if dataset is None
                else GoldenDataset.from_dict(dataset.to_dict())
            )

    def upsert(self, dataset: GoldenDataset) -> GoldenDataset:
        """Insert or replace dataset."""
        with _LOCK:
            self._datasets[dataset.dataset_id] = dataset
            self._persist()
            return GoldenDataset.from_dict(dataset.to_dict())

    def delete(self, dataset_id: str) -> bool:
        """Delete dataset if present."""
        with _LOCK:
            if dataset_id not in self._datasets:
                return False
            del self._datasets[dataset_id]
            self._persist()
            return True

    def clear(self) -> None:
        """Clear store (tests)."""
        with _LOCK:
            self._datasets.clear()
            self._persist()

    def export_all(self) -> dict[str, Any]:
        """Export raw snapshot."""
        with _LOCK:
            return {
                "datasets": [item.to_dict() for item in self._datasets.values()],
            }


_STORE: DatasetStore | None = None


def get_store() -> DatasetStore:
    """Return process-wide store."""
    global _STORE
    if _STORE is None:
        _STORE = DatasetStore()
    return _STORE


def reset_store(data_dir: Path | None = None) -> DatasetStore:
    """Reset process store (tests)."""
    global _STORE
    _STORE = DatasetStore(data_dir=data_dir)
    return _STORE
