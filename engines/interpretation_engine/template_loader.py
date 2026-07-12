"""
interpretation_engine/template_loader.py

Nạp template diễn giải từ JSON.
"""

from __future__ import annotations

import json
from pathlib import Path


class TemplateLoader:

    def __init__(self, template_root: Path):

        self.root = Path(template_root)

        self.cache: dict[str, dict] = {}

    def load(self, filename: str) -> dict:

        if filename in self.cache:
            return self.cache[filename]

        path = self.root / filename

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as f:

            data = json.load(f)

        self.cache[filename] = data

        return data

    def lookup(
        self,
        filename: str,
        code: str,
    ) -> dict | None:

        data = self.load(filename)

        return data.get(code)
