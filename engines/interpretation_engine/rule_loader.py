"""
Rule Loader
===========

Nạp Rule Database cho Interpretation Engine.

Pipeline:

Rule Database
      ↓
Rule Loader
      ↓
Rule Matcher
      ↓
Rule Scoring
      ↓
Interpretation Builder
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


SUPPORTED_FORMAT = {"csv", "json"}


class RuleLoader:
    """
    Đọc và chuẩn hóa Rule Database.
    """

    def __init__(self, rule_path: Optional[str] = None):

        self.rule_path = rule_path
        self.cache: List[Dict[str, Any]] = []

    # ==========================================================
    # Main
    # ==========================================================

    def load(self, path: Optional[str] = None) -> List[Dict[str, Any]]:

        file_path = path or self.rule_path

        # WP4: default to Knowledge Base when no explicit file
        if not file_path:
            if self.cache:
                return self.cache
            from .knowledge_rule_loader import KnowledgeRuleLoader

            self.cache = KnowledgeRuleLoader().load()
            return self.cache

        if self.cache:
            return self.cache

        path_obj = Path(file_path)
        if path_obj.is_dir():
            from .knowledge_rule_loader import KnowledgeRuleLoader

            self.cache = KnowledgeRuleLoader(path_obj).load()
            return self.cache

        extension = path_obj.suffix.lower().replace(".", "")

        if extension not in SUPPORTED_FORMAT:
            raise ValueError(f"Unsupported rule format: {extension}")

        if extension == "csv":
            rules = self.load_csv(file_path)
        else:
            rules = self.load_json(file_path)

        self.cache = self.normalize_rules(rules)

        return self.cache

    # ==========================================================
    # CSV
    # ==========================================================

    def load_csv(self, file_path: str) -> List[Dict[str, Any]]:

        with open(file_path, encoding="utf-8") as f:

            reader = csv.DictReader(f)

            return [dict(row) for row in reader]

    # ==========================================================
    # JSON
    # ==========================================================

    def load_json(self, file_path: str) -> List[Dict[str, Any]]:

        with open(file_path, encoding="utf-8") as f:

            return json.load(f)

    # ==========================================================
    # Normalize
    # ==========================================================

    def normalize_rules(
        self,
        rules: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        result = []

        for rule in rules:

            result.append(

                {
                    "rule_id": rule.get("rule_id", "").strip(),

                    "rule_name": rule.get("rule_name", "").strip(),

                    "category": rule.get("category", "").strip(),

                    "layer": rule.get("layer", "default").strip(),

                    "section": rule.get("section", "general").strip(),

                    "condition": self.parse_condition(
                        rule.get("condition", "")
                    ),

                    "description": rule.get(
                        "description",
                        ""
                    ).strip(),

                    "polarity": rule.get(
                        "polarity",
                        "neutral"
                    ).strip(),

                    "priority": self.convert_number(
                        rule.get("priority", 99)
                    ),

                    "score": self.convert_number(
                        rule.get("score", 0)
                    ),

                    "tags": self.parse_tags(
                        rule.get("tags", "")
                    )
                }

            )

        return result

    # ==========================================================
    # Parse Condition
    # ==========================================================

    def parse_condition(
        self,
        value: Any
    ) -> Dict[str, Any]:

        """
        Hỗ trợ:

        nhat_chu=Canh Kim

        season=Xuan;strength=manh

        than=Ty;chi=Suu
        """

        if not value:
            return {}

        if isinstance(value, dict):
            return value

        result = {}

        for item in str(value).split(";"):

            item = item.strip()

            if not item:
                continue

            if "=" not in item:
                continue

            key, val = item.split("=", 1)

            result[key.strip()] = val.strip()

        return result

    # ==========================================================
    # Parse Tags
    # ==========================================================

    def parse_tags(
        self,
        value: Any
    ) -> List[str]:

        if not value:
            return []

        if isinstance(value, list):
            return value

        return [

            x.strip()

            for x in str(value).split(",")

            if x.strip()

        ]

    # ==========================================================
    # Filter
    # ==========================================================

    def filter_by_category(
        self,
        rules,
        category
    ):

        return [

            r

            for r in rules

            if r["category"] == category

        ]

    def filter_by_layer(
        self,
        rules,
        layer
    ):

        return [

            r

            for r in rules

            if r["layer"] == layer

        ]

    # ==========================================================
    # Cache
    # ==========================================================

    def clear_cache(self):

        self.cache = []

    # ==========================================================
    # Number
    # ==========================================================

    def convert_number(
        self,
        value: Any
    ):

        if value in ("", None):
            return 0

        try:
            return int(value)

        except (ValueError, TypeError):

            try:
                return float(value)

            except (ValueError, TypeError):
                return 0


# ==============================================================
# Service
# ==============================================================

def load_rules(rule_path: str):

    return RuleLoader(rule_path).load()
