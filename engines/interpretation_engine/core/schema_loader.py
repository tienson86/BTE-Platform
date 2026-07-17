from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class SchemaLoader:
    """
    Quản lý và nạp các JSON Schema của Interpretation Engine.
    """

    def __init__(self, schema_dir: str | Path):
        self.schema_dir = Path(schema_dir)
        self._cache: dict[str, dict[str, Any]] = {}

    def load(self, name: str) -> dict[str, Any]:
        """
        Nạp một schema theo tên.
        Ví dụ:
            load("rule_schema")
        """
        filename = f"{name}.json"

        if filename in self._cache:
            return self._cache[filename]

        path = self.schema_dir / filename

        if not path.exists():
            raise FileNotFoundError(f"Không tìm thấy schema: {filename}")

        with open(path, "r", encoding="utf-8") as f:
            schema = json.load(f)

        self._cache[filename] = schema

        return schema

    def clear_cache(self):
        self._cache.clear()

    def list_schemas(self):
        return sorted(
            p.stem
            for p in self.schema_dir.glob("*.json")
        )
