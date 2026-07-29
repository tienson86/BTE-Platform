"""
condition_parser.py
===================

Parser điều kiện Rule.

Nhiệm vụ
--------
Chuyển chuỗi điều kiện thành các token và biểu thức
để RuleMatcher đánh giá.

Ví dụ:

strength == WEAK
AND
useful_god == FIRE

↓

[
    Condition("strength","==","WEAK"),
    Logic("AND"),
    Condition("useful_god","==","FIRE")
]
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Union


# ==========================================================
# Operator
# ==========================================================

class Operator(str, Enum):

    EQ = "=="

    NE = "!="

    GT = ">"

    LT = "<"

    GTE = ">="

    LTE = "<="

    CONTAINS = "contains"

    NOT_CONTAINS = "not_contains"

    EXISTS = "exists"

    NOT_EXISTS = "not_exists"


# ==========================================================
# Logic
# ==========================================================

class Logic(str, Enum):

    AND = "AND"

    OR = "OR"

    NOT = "NOT"


# ==========================================================
# AST Node
# ==========================================================

@dataclass(slots=True)
class ConditionNode:

    field: str

    operator: Operator

    value: str | None = None


@dataclass(slots=True)
class LogicNode:

    logic: Logic


ASTNode = Union[
    ConditionNode,
    LogicNode,
]


# ==========================================================
# Parser
# ==========================================================

class ConditionParser:

    """
    Parser Rule Condition.
    """

    OPERATORS = [

        ">=",
        "<=",

        "==",
        "!=",

        ">",

        "<",

        "contains",

        "not_contains",

        "exists",

        "not_exists",
    ]

    LOGIC = [

        "AND",

        "OR",

        "NOT",
    ]

    # ------------------------------------------------------

    def parse(
        self,
        condition: str,
    ) -> List[ASTNode]:

        nodes: List[ASTNode] = []

        if not condition:

            return nodes

        tokens = condition.split()

        current = []

        for token in tokens:

            if token in self.LOGIC:

                if current:

                    nodes.append(
                        self.parse_expression(
                            current
                        )
                    )

                    current = []

                nodes.append(
                    LogicNode(
                        Logic(token)
                    )
                )

            else:

                current.append(token)

        if current:

            nodes.append(
                self.parse_expression(
                    current
                )
            )

        return nodes

    # ------------------------------------------------------

    def parse_expression(
        self,
        tokens: List[str],
    ) -> ConditionNode:

        text = " ".join(tokens)

        for op in self.OPERATORS:

            if op in text:

                parts = text.split(op)

                left = parts[0].strip()

                right = None

                if len(parts) > 1:

                    right = parts[1].strip()

                return ConditionNode(

                    field=left,

                    operator=Operator(op),

                    value=right,

                )

        raise ValueError(

            f"Không thể phân tích điều kiện: {text}"

        )
