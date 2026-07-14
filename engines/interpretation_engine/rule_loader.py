"""
rule_loader.py
==============

Quản lý và nạp Rule Database cho Interpretation Engine.

Chức năng:

- Đọc Rule từ Database
- Cache Rule
- Kiểm tra schema
- Trả về Rule theo module/category/id

Không thực hiện:
- Match Rule
- Scoring
- Interpretation

Các chức năng đó thuộc các module khác.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Optional


class RuleLoader:

    """
    Rule Repository.
    """

    REQUIRED_COLUMNS = {
        "rule_id",
        "module",
        "category",
        "condition",
        "priority",
        "weight",
        "enabled",
    }

    def __init__(self, database_root: Path):

        self.database_root = Path(database_root)

        self._cache: Dict[str, List[dict]] = {}

    # =====================================================
    # Public API
    # =====================================================

    def load_all(self) -> List[dict]:
        """
        Đọc toàn bộ Rule Database.
        """

        rules = []

        for csv_file in self.database_root.rglob("*.csv"):

            rules.extend(
                self.load_file(csv_file)
            )

        return rules

    def load_module(self, module: str) -> List[dict]:
        """
        Đọc toàn bộ Rule của một module.

        Ví dụ:

        03_dung_than
        """

        path = self.database_root / module

        rules = []

        for csv_file in path.glob("*.csv"):

            rules.extend(
                self.load_file(csv_file)
            )

        return rules

    def load_category(
        self,
        module: str,
        category: str,
    ) -> List[dict]:

        rules = self.load_module(module)

        return [
            r
            for r in rules
            if r.get("category") == category
        ]

    def load_rule(
        self,
        rule_id: str,
    ) -> Optional[dict]:

        for rule in self.load_all():

            if rule["rule_id"] == rule_id:
                return rule

        return None

    def clear_cache(self):

        self._cache.clear()

    # =====================================================
    # Internal
    # =====================================================

    def load_file(
        self,
        file_path: Path,
    ) -> List[dict]:

        key = str(file_path)

        if key in self._cache:
            return self._cache[key]

        rules = []

        with open(
            file_path,
            encoding="utf-8-sig",
        ) as f:

            reader = csv.DictReader(f)

            self.validate_columns(reader.fieldnames)

            for row in reader:

                if (
                    row.get("enabled", "true")
                    .lower()
                    != "true"
                ):
                    continue

                rules.append(row)

        self._cache[key] = rules

        return rules

    def validate_columns(
        self,
        columns,
    ):

        if columns is None:
            raise ValueError("CSV không có header.")

        missing = (
            self.REQUIRED_COLUMNS
            - set(columns)
        )

        if missing:

            raise ValueError(
                "Thiếu cột: "
                + ", ".join(sorted(missing))
            )

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):

        total = 0

        modules = {}

        for rule in self.load_all():

            total += 1

            module = rule["module"]

            modules[module] = (
                modules.get(module, 0)
                + 1
            )

        return {
            "total_rules": total,
            "modules": modules,
        }
