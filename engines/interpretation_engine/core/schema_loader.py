"""
BTE Platform
Interpretation Engine

Schema Loader

Quản lý toàn bộ JSON Schema dùng trong Interpretation Engine.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class SchemaNotFoundError(FileNotFoundError):
    """Không tìm thấy schema."""


class SchemaLoader:
    """
    Nạp và cache toàn bộ JSON Schema.
    """

    def __init__(self, schema_dir: str | Path):

        self.schema_dir = Path(schema_dir)

        self._cache: dict[str, dict[str, Any]] = {}

    def load(self, schema_name: str) -> dict:

        filename = schema_name

        if not filename.endswith(".json"):
            filename += ".json"

        if filename in self._cache:
            return self._cache[filename]

        path = self.schema_dir / filename

        if not path.exists():
            raise SchemaNotFoundError(str(path))

        with open(path, "r", encoding="utf-8") as f:
            schema = json.load(f)

        self._cache[filename] = schema

        return schema

    def exists(self, schema_name: str) -> bool:

        filename = schema_name

        if not filename.endswith(".json"):
            filename += ".json"

        return (self.schema_dir / filename).exists()

    def list(self):

        return sorted(

            file.stem

            for file in self.schema_dir.glob("*.json")

        )

    def clear_cache(self):

        self._cache.clear()

    def reload(self, schema_name: str):

        filename = schema_name

        if not filename.endswith(".json"):
            filename += ".json"

        self._cache.pop(filename, None)

        return self.load(filename)
