"""
contains.py
===========

Operator xử lý:

contains
"""

from __future__ import annotations

from ...models.context import InterpretationContext
from ...models.rule import Rule
from ..condition_parser import ConditionNode

from .base import BaseOperator


class ContainsOperator(BaseOperator):
    """
    Toán tử contains
    """

    name = "contains"

    priority = 100

    def evaluate(
        self,
        context: InterpretationContext,
        node: ConditionNode,
        rule: Rule | None = None,
    ) -> bool:

        value = self.resolve(
            context,
            node.field,
        )

        if value is None:
            return False

        target = self.normalize(node.value)

        if isinstance(value, (list, tuple, set)):
            return target in [
                self.normalize(v)
                for v in value
            ]

        if isinstance(value, dict):
            return target in value

        return target in self.normalize(str(value))
