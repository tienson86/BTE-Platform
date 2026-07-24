"""JSON-backed file storage (WP11 — no SQL/ORM)."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("bte.applications.storage")


class JsonStore:
    """Read/write a single JSON document (object or list) atomically-ish."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def exists(self) -> bool:
        """True if the JSON file exists."""
        return self.path.exists()

    def load(self, default: Any = None) -> Any:
        """Load JSON; return ``default`` when file is missing."""
        if not self.path.exists():
            return default if default is not None else {}
        try:
            with self.path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to load %s: %s", self.path, exc)
            return default if default is not None else {}

    def save(self, data: Any) -> None:
        """Persist JSON with UTF-8 and indentation."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2, default=str)
        tmp.replace(self.path)

    def load_dict(self) -> dict[str, Any]:
        """Load a JSON object; empty dict if missing/invalid."""
        data = self.load(default={})
        return data if isinstance(data, dict) else {}

    def load_list(self) -> list[Any]:
        """Load a JSON array; empty list if missing/invalid."""
        data = self.load(default=[])
        return data if isinstance(data, list) else []
