"""
Base Loader.

Lớp cơ sở cho tất cả Loader trong BTE Platform.
"""

from __future__ import annotations

from abc import ABC
from pathlib import Path
from typing import Any

import json
import pandas as pd


class BaseLoader(ABC):
    """
    Loader cơ sở.

    Hỗ trợ:
        - CSV
        - JSON
        - Cache
    """

    def __init__(self, root_path: str | Path):

        self.root_path = Path(root_path)

        self._cache: dict[str, Any] = {}

    def exists(self, filename: str) -> bool:

        return (self.root_path / filename).exists()

    def load_csv(self, filename: str) -> pd.DataFrame:

        if filename in self._cache:
            return self._cache[filename]

        file = self.root_path / filename

        dataframe = pd.read_csv(
            file,
            encoding="utf-8"
        )

        self._cache[filename] = dataframe

        return dataframe

    def load_json(self, filename: str):

        if filename in self._cache:
            return self._cache[filename]

        file = self.root_path / filename

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as fp:

            data = json.load(fp)

        self._cache[filename] = data

        return data

    def clear_cache(self):

        self._cache.clear()

    def cache_size(self) -> int:

        return len(self._cache)
