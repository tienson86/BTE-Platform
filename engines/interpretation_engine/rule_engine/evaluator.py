"""
evaluator.py
============

Đánh giá AST của Rule.

Parser
    ↓
AST
    ↓
Evaluator
    ↓
True / False
"""

from __future__ import annotations

from .condition_parser import (
    ConditionNode,
    LogicNode,
    Logic,
)

from .registry import OperatorRegistry

from ..models.context import InterpretationContext
from ..models.rule import Rule


class Evaluator:

    def __init__(
        self,
        registry: OperatorRegistry,
    ):

        self.registry = registry

    # =====================================================

    def evaluate(
        self,
        context: InterpretationContext,
        rule: Rule,
        ast,
    ) -> bool:

        if not ast:
            return True

        result = None

        logic = Logic.AND

        for node in ast:

            if isinstance(node, LogicNode):

                logic = node.logic

                continue

            value = self.evaluate_node(
                context,
                rule,
                node,
            )

            if result is None:

                result = value

                continue

            if logic == Logic.AND:

                result = result and value

            elif logic == Logic.OR:

                result = result or value

        return bool(result)

    # =====================================================

    def evaluate_node(
        self,
        context,
        rule,
        node: ConditionNode,
    ) -> bool:

        operator = self.registry.get(
            node.operator.value
        )

        return operator.evaluate(
            context=context,
            node=node,
            rule=rule,
        )
