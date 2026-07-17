"""
rule_matcher.py
===============

BTE Platform
Interpretation Engine

Rule Matcher

Nhiệm vụ
---------
- Nhận danh sách Rule
- Parse điều kiện
- Evaluate điều kiện
- Trả về Rule phù hợp

RuleMatcher KHÔNG:

- Parse Condition
- Evaluate Expression
- Score Rule
- Resolve Conflict
"""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from .condition_parser import ConditionParser
from .condition_evaluator import ConditionEvaluator


class RuleMatcher:
    """
    Match Rule với InterpretationContext.
    """

    def __init__(
        self,
        parser: ConditionParser | None = None,
        evaluator: ConditionEvaluator | None = None,
    ):

        self.parser = parser or ConditionParser()

        self.evaluator = evaluator or ConditionEvaluator()

    # =====================================================
    # Public API
    # =====================================================

    def match(
        self,
        context: Any,
        rules: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Match danh sách Rule.
        """

        if not rules:
            return []

        matched: List[Dict[str, Any]] = []

        for rule in rules:

            if not self.validate_rule(rule):
                continue

            if self.match_one(context, rule):
                matched.append(rule)

        return self.sort_by_priority(matched)

    # =====================================================
    # Match One
    # =====================================================

    def match_one(
        self,
        context: Any,
        rule: Dict[str, Any],
    ) -> bool:
        """
        Match một Rule.
        """

        condition = rule.get("condition")

        # Không có điều kiện
        if not condition:
            return True

        try:

            nodes = self.parser.parse(condition)

        except Exception:

            return False

        return self.evaluator.evaluate(
            context=context,
            nodes=nodes,
        )

    def match_all(
        self,
        context: Any,
        rules: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        return self.match(
            context=context,
            rules=rules,
        )

    # =====================================================
    # Validation
    # =====================================================

    @staticmethod
    def validate_rule(
        rule: Dict[str, Any],
    ) -> bool:

        if not isinstance(rule, dict):
            return False

        return True
    # =====================================================
    # Filter
    # =====================================================

    def filter_by_category(
        self,
        rules: List[Dict[str, Any]],
        category: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Lọc Rule theo category.
        """

        if not category:
            return list(rules)

        return [
            rule
            for rule in rules
            if rule.get("category") == category
        ]

    def filter_by_layer(
        self,
        rules: List[Dict[str, Any]],
        layer: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Lọc Rule theo layer.
        """

        if not layer:
            return list(rules)

        return [
            rule
            for rule in rules
            if rule.get("layer") == layer
        ]

    # =====================================================
    # Group
    # =====================================================

    def group_by_category(
        self,
        rules: List[Dict[str, Any]],
    ) -> Dict[str, List[Dict[str, Any]]]:

        groups: Dict[str, List[Dict[str, Any]]] = {}

        for rule in rules:

            category = rule.get("category", "default")

            groups.setdefault(category, []).append(rule)

        return groups

    def group_by_layer(
        self,
        rules: List[Dict[str, Any]],
    ) -> Dict[str, List[Dict[str, Any]]]:

        groups: Dict[str, List[Dict[str, Any]]] = {}

        for rule in rules:

            layer = rule.get("layer", "default")

            groups.setdefault(layer, []).append(rule)

        return groups

    # =====================================================
    # Sort
    # =====================================================

    def sort_by_priority(
        self,
        rules: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Sắp xếp theo priority giảm dần.
        """

        return sorted(
            rules,
            key=lambda r: int(r.get("priority", 0)),
            reverse=True,
        )

    # =====================================================
    # Statistics
    # =====================================================

    def count(
        self,
        rules: List[Dict[str, Any]],
    ) -> int:
        """
        Đếm số Rule.
        """

        return len(rules)

    def is_empty(
        self,
        rules: List[Dict[str, Any]],
    ) -> bool:
        """
        Kiểm tra danh sách Rule rỗng.
        """

        return len(rules) == 0

    # =====================================================
    # Utility
    # =====================================================

    def first(
        self,
        rules: List[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:
        """
        Lấy Rule đầu tiên.
        """

        if not rules:
            return None

        return rules[0]

    def last(
        self,
        rules: List[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:
        """
        Lấy Rule cuối cùng.
        """

        if not rules:
            return None

        return rules[-1]
