"""
not_equal.py
============

Operator xử lý:

!=
"""

from __future__ import annotations

from ...models.context import InterpretationContext
from ...models.rule import Rule
from ..condition_parser import ConditionNode

from .base import BaseOperator


class NotEqualOperator(BaseOperator):
    """
    Toán tử !=
    """

    name = "!="

    priority = 100

    def evaluate(
        self,
        context: InterpretationContext,
        node: ConditionNode,
        rule: Rule | None = None,
    ) -> bool:

        left = self.resolve(
            context,
            node.field,
        )

        if left is None:
            return False

        return self.normalize(left) != self.normalize(node.value)
