"""
exists.py
=========

Operator xử lý:

exists
"""

from __future__ import annotations

from ...models.context import InterpretationContext
from ...models.rule import Rule
from ..condition_parser import ConditionNode

from .base import BaseOperator


class ExistsOperator(BaseOperator):
    """
    Toán tử exists
    """

    name = "exists"

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

        if isinstance(value, str):
            return value.strip() != ""

        if isinstance(value, (list, tuple, set, dict)):
            return len(value) > 0

        return True
