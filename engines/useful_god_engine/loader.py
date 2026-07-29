"""Loader for Useful God rule database."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


RULE_FILES: tuple[tuple[str, str], ...] = (
    ("strength", "01_strength_rules.csv"),
    ("season", "02_season_rules.csv"),
    ("temperature", "03_temperature_rules.csv"),
    ("flow", "04_flow_rules.csv"),
    ("special", "06_special_rules.csv"),
)


class UsefulGodLoader:
    def __init__(self, database_path: str):
        self.database_path = Path(database_path)
        self._cache: dict[str, pd.DataFrame] = {}

    def load_csv(self, filename: str) -> pd.DataFrame:
        if filename in self._cache:
            return self._cache[filename]
        path = self.database_path / filename
        if not path.exists():
            raise FileNotFoundError(path)
        df = pd.read_csv(path, encoding="utf-8")
        self._cache[filename] = df
        return df

    def load_rule_groups(self) -> dict[str, list[dict[str, Any]]]:
        out: dict[str, list[dict[str, Any]]] = {}
        for group, filename in RULE_FILES:
            df = self.load_csv(filename)
            records = df.to_dict("records")
            for record in records:
                record.setdefault("rule_group", group)
            out[group] = records
        return out

    def load_priority_rules(self) -> list[dict[str, Any]]:
        df = self.load_csv("05_priority_rules.csv")
        return df.to_dict("records")

    def clear_cache(self) -> None:
        self._cache.clear()

    def cache_size(self) -> int:
        return len(self._cache)
