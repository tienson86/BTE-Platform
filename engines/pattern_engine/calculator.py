"""
Pattern Calculator.

Điều phối toàn bộ quá trình nhận diện Cách Cục.
"""

from __future__ import annotations

import json
from typing import Any

import pandas as pd

from .loader import PatternLoader
from .matcher import PatternMatcher
from .validator import PatternValidator


class PatternCalculator:

    def __init__(self, loader: PatternLoader):

        self.loader = loader
        self.matcher = PatternMatcher()

    def calculate(self, context):

        result = {
            "success": True,
            "pattern": None,
            "matched_rules": [],
            "score": 0,
            "priority": 0,
        }

        if not self.loader.rules_exist():
            result["success"] = False
            result["error"] = (
                "rules.csv / 01_main_pattern.csv not found "
                f"in {self.loader.database_path}"
            )
            return result

        df = self.loader.load_rules()

        PatternValidator.validate_dataframe(df)

        rules = df.to_dict("records")

        for rule in rules:

            rule = self._normalize_rule(rule)

            if not rule.get("enabled", True):
                continue

            if self.matcher.match(context, rule):

                result["matched_rules"].append(
                    rule["rule_id"]
                )

                if rule["priority"] >= result["priority"]:

                    result["priority"] = rule["priority"]
                    result["pattern"] = rule["pattern"]
                    result["score"] = rule.get(
                        "score",
                        0
                    )

        if not result["matched_rules"]:
            result["success"] = False
            result["error"] = "no pattern rules matched"

        return result

    def _normalize_rule(self, rule: dict[str, Any]) -> dict[str, Any]:
        """Normalize CSV row types for matcher."""

        normalized = dict(rule)
        normalized["conditions"] = self._parse_conditions(
            normalized.get("conditions")
        )

        if "priority" in normalized:
            normalized["priority"] = int(normalized["priority"])

        if "score" in normalized and normalized["score"] is not None:
            try:
                if pd.isna(normalized["score"]):
                    normalized["score"] = 0
                else:
                    normalized["score"] = float(normalized["score"])
            except TypeError:
                normalized["score"] = float(normalized["score"])

        if "enabled" in normalized:
            value = normalized["enabled"]
            if isinstance(value, str):
                normalized["enabled"] = value.strip().lower() in {
                    "1",
                    "true",
                    "yes",
                    "y",
                }
            elif pd.isna(value):
                normalized["enabled"] = True
            else:
                normalized["enabled"] = bool(value)

        return normalized

    @staticmethod
    def _parse_conditions(raw: Any) -> list:
        """Parse conditions cell from CSV into list[dict]."""

        if raw is None:
            return []

        try:
            if pd.isna(raw):
                return []
        except TypeError:
            pass

        if isinstance(raw, list):
            return raw

        if isinstance(raw, str):
            text = raw.strip()
            if not text or text == "[]":
                return []
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                return []
            if isinstance(parsed, list):
                return parsed
            return []

        return []
