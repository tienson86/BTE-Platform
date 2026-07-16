"""
Tokenizer

Chuyển chuỗi điều kiện thành danh sách token.

Ví dụ:

strength >= 70

↓

["strength", ">=", "70"]
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Token:

    type: str

    value: str


class Tokenizer:

    OPERATORS = [
        ">=",
        "<=",
        "==",
        "!=",
        ">",
        "<",
        "(",
        ")",
    ]

    KEYWORDS = {
        "AND",
        "OR",
        "NOT",
        "IN",
    }

    def tokenize(
        self,
        expression: str
    ) -> List[Token]:

        expr = expression

        #
        # Tách toán tử
        #

        for op in sorted(
            self.OPERATORS,
            key=len,
            reverse=True
        ):

            expr = expr.replace(op, f" {op} ")

        words = expr.split()

        tokens = []

        for word in words:

            upper = word.upper()

            if upper in self.KEYWORDS:

                tokens.append(
                    Token(
                        "KEYWORD",
                        upper
                    )
                )

            elif word in self.OPERATORS:

                tokens.append(
                    Token(
                        "OPERATOR",
                        word
                    )
                )

            elif word.replace(".", "", 1).isdigit():

                tokens.append(
                    Token(
                        "NUMBER",
                        word
                    )
                )

            else:

                tokens.append(
                    Token(
                        "IDENTIFIER",
                        word
                    )
                )

        return tokens
