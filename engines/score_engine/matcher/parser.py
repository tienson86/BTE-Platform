"""
Expression Parser

Token

↓

AST
"""

from dataclasses import dataclass
from typing import List

from .tokenizer import Token


@dataclass
class BinaryExpression:

    left: str

    operator: str

    right: str


class ExpressionParser:

    def parse(
        self,
        tokens: List[Token]
    ):

        #
        # V1:
        #
        # identifier operator value
        #

        if len(tokens) != 3:

            raise ValueError(
                "Biểu thức chưa được hỗ trợ."
            )

        left = tokens[0].value

        operator = tokens[1].value

        right = tokens[2].value

        return BinaryExpression(
            left,
            operator,
            right
        )
