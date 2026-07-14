"""
rule_matcher.py
===============

Bộ máy so khớp Rule của Interpretation Engine.

Nhiệm vụ
--------
- Phân tích điều kiện Rule
- Đối chiếu với InterpretationContext
- Trả về RuleResult

Không thực hiện:
- Chấm điểm
- Sắp xếp ưu tiên
- Sinh câu luận
"""

from __future__ import annotations

from typing import Iterable, List

from .models.context import InterpretationContext
from .models.rule import Rule
from .models.rule_result import RuleResult


class RuleMatcher:
    """
    Bộ máy so khớp Rule.
    """

    # =====================================================
    # Public API
    # =====================================================

    def match(
        self,
        context: InterpretationContext,
        rules: Iterable[Rule],
    ) -> List[RuleResult]:

        results: List[RuleResult] = []

        for rule in rules:

            matched = self.evaluate(
                rule.condition,
                context,
            )

            result = RuleResult(
                rule=rule,
                matched=matched,
                priority=rule.priority,
                score=rule.weight if matched else 0.0,
                text=rule.result if matched else "",
            )

            results.append(result)

        return results

    # =====================================================
    # Evaluate
    # =====================================================

    def evaluate(
        self,
        condition: str,
        context: InterpretationContext,
    ) -> bool:

        if not condition:
            return True

        tokens = [
            t.strip()
            for t in condition.split("AND")
            if t.strip()
        ]

        for token in tokens:

            if not self.evaluate_expression(
                token,
                context,
            ):
                return False

        return True

    # =====================================================
    # Expression
    # =====================================================

    def evaluate_expression(
        self,
        expression: str,
        context: InterpretationContext,
    ) -> bool:

        # ==
        if "==" in expression:

            left, right = expression.split("==", 1)

            return self.compare(
                context.resolve(left.strip()),
                right.strip(),
            )

        # !=
        if "!=" in expression:

            left, right = expression.split("!=", 1)

            return (
                context.resolve(left.strip())
                != right.strip()
            )

        # contains

        if "contains" in expression:

            left, right = expression.split(
                "contains",
                1,
            )

            return self.contains(
                context.resolve(left.strip()),
                right.strip(),
            )

        # exists

        if expression.endswith("exists"):

            field = expression.replace(
                "exists",
                "",
            ).strip()

            return context.resolve(field) is not None

        raise ValueError(
            f"Không hiểu biểu thức: {expression}"
        )

    # =====================================================
    # Compare
    # =====================================================

    def compare(
        self,
        left,
        right,
    ) -> bool:

        if left is None:
            return False

        return str(left) == str(right)

    def contains(
        self,
        left,
        right,
    ) -> bool:

        if left is None:
            return False

        if isinstance(left, str):

            return right in left

        if isinstance(left, list):

            return right in left

        return False
