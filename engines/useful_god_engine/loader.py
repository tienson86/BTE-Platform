"""Loader for Useful God rule database."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import json

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
        self._validate_rule_pack(out)
        return out

    @staticmethod
    def _validate_rule_pack(grouped: dict[str, list[dict[str, Any]]]) -> None:
        seen: set[str] = set()
        for group, rules in grouped.items():
            for rule in rules:
                rule_id = str(rule.get("rule_id") or "").strip()
                if not rule_id:
                    raise ValueError(f"Useful God rule without rule_id in {group}")
                if rule_id in seen:
                    raise ValueError(f"Duplicate Useful God rule_id: {rule_id}")
                seen.add(rule_id)
                raw_conditions = rule.get("conditions")
                try:
                    conditions = (
                        raw_conditions
                        if isinstance(raw_conditions, list)
                        else json.loads(str(raw_conditions or "[]"))
                    )
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid conditions JSON for {rule_id}") from exc
                if not isinstance(conditions, list):
                    raise ValueError(f"Conditions must be a list for {rule_id}")
                favorable = UsefulGodLoader._json_tokens(rule.get("favorable_gods"))
                unfavorable = UsefulGodLoader._json_tokens(rule.get("unfavorable_gods"))
                overlap = favorable & unfavorable
                if overlap:
                    raise ValueError(
                        f"Useful God rule {rule_id} has favorable/unfavorable overlap: "
                        f"{sorted(overlap)}"
                    )

    @staticmethod
    def _json_tokens(raw: Any) -> set[str]:
        if raw is None or (isinstance(raw, float) and pd.isna(raw)):
            return set()
        if isinstance(raw, list):
            return {str(item) for item in raw}
        text = str(raw).strip()
        if not text:
            return set()
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid favorable/unfavorable JSON") from exc
        if not isinstance(parsed, list):
            raise ValueError("Favorable/unfavorable values must be JSON lists")
        return {str(item) for item in parsed}

    def load_priority_rules(self) -> list[dict[str, Any]]:
        df = self.load_csv("05_priority_rules.csv")
        return df.to_dict("records")

    def clear_cache(self) -> None:
        self._cache.clear()

    def cache_size(self) -> int:
        return len(self._cache)
