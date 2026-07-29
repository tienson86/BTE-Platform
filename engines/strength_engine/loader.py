"""Loader for Strength Engine rule database."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


RULE_FILES: tuple[tuple[str, str], ...] = (
    ("season", "01_season_rules.csv"),
    ("root", "02_root_rules.csv"),
    ("support", "03_support_rules.csv"),
    ("control", "04_control_rules.csv"),
    ("drain", "05_flow_rules.csv"),
    ("special", "07_special_rules.csv"),
)


class StrengthLoader:
    """Read-only loader for strength rule CSV files."""

    def __init__(self, database_path: str) -> None:
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
        combination: list[dict[str, Any]] = []
        for group, filename in RULE_FILES:
            df = self.load_csv(filename)
            records: list[dict[str, Any]] = []
            for record in df.to_dict("records"):
                target = str(record.get("score_target") or group)
                if target == "combination":
                    item = dict(record)
                    item["rule_group"] = "combination"
                    combination.append(item)
                    continue
                item = dict(record)
                item.setdefault("rule_group", group)
                records.append(item)
            out[group] = records
        if combination:
            out["combination"] = combination
        return out

    def load_priority_rules(self) -> list[dict[str, Any]]:
        df = self.load_csv("06_priority_rules.csv")
        return df.to_dict("records")

    def load_level_rules(self) -> list[dict[str, Any]]:
        rows = self.load_priority_rules()
        return [r for r in rows if str(r.get("score_target") or "") == "level"]

    def load_config(self) -> dict[str, float]:
        df = self.load_csv("09_conditions.csv")
        config: dict[str, float] = {
            "baseline": 50.0,
            "scale": 100.0,
            "strong_threshold": 0.65,
            "weak_threshold": 0.35,
        }
        for row in df.to_dict("records"):
            if str(row.get("score_target") or "") != "config":
                continue
            rule_id = str(row.get("rule_id") or "")
            score = float(row.get("score") or 0.0)
            level = str(row.get("strength_level") or "")
            if rule_id == "cfg_baseline":
                config["baseline"] = score
            elif rule_id == "cfg_scale":
                config["scale"] = score
            elif rule_id == "cfg_strong_threshold":
                config["strong_threshold"] = score
            elif rule_id == "cfg_weak_threshold":
                config["weak_threshold"] = score
            elif level == "strong":
                config["strong_threshold"] = score if score > 0 else config["strong_threshold"]
            elif level == "weak":
                config["weak_threshold"] = score if score > 0 else config["weak_threshold"]
        return config

    def load_examples(self) -> list[dict[str, Any]]:
        df = self.load_csv("08_examples.csv")
        return df.to_dict("records")

    def clear_cache(self) -> None:
        self._cache.clear()

    def cache_size(self) -> int:
        return len(self._cache)
