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
