"""
Tính điểm và xác định Cách Cục.
"""

from typing import List

from ..models.pattern_rule import PatternRule


class StructureCalculator:

    def calculate(
        self,
        rules: List[PatternRule]
    ) -> PatternRule | None:

        if not rules:
            return None

        return max(
            rules,
            key=lambda r: (
                r.priority,
                r.score
            )
        )
