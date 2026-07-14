"""
tokenizer.py
============

Tokenizer của Rule Engine.

Chuyển Rule Condition thành Token.

Ví dụ:

strength == WEAK
AND
useful_god == FIRE

↓

IDENT(strength)
EQ
IDENT(WEAK)
AND
IDENT(useful_god)
EQ
IDENT(FIRE)
"""

from __future__ import annotations

import re

from dataclasses import dataclass
from enum import Enum
from typing import List


# ==========================================================
# Token Type
# ==========================================================

class TokenType(str, Enum):

    IDENT = "IDENT"

    STRING = "STRING"

    NUMBER = "NUMBER"

    OPERATOR = "OPERATOR"

    LOGIC = "LOGIC"

    LPAREN = "("

    RPAREN = ")"

    COMMA = ","

    EOF = "EOF"


# ==========================================================
# Token
# ==========================================================

@dataclass(slots=True)
class Token:

    type: TokenType

    value: str


# ==========================================================
# Tokenizer
# ==========================================================

class Tokenizer:

    TOKEN_REGEX = re.compile(
        r"""
        (>=|<=|==|!=|>|<)             |
        (\bcontains\b)                |
        (\bnot_contains\b)            |
        (\bexists\b)                  |
        (\bnot_exists\b)              |
        (\bAND\b|\bOR\b|\bNOT\b)      |
        (\()                          |
        (\))                          |
        (,)                           |
        ("[^"]*")                     |
        ([A-Za-z_][A-Za-z0-9_.]*)     |
        (\d+\.\d+|\d+)
        """,
        re.VERBOSE,
    )

    # ------------------------------------------------------

    def tokenize(
        self,
        text: str,
    ) -> List[Token]:

        tokens: List[Token] = []

        for match in self.TOKEN_REGEX.finditer(text):

            value = match.group(0)

            if value in {

                "==",
                "!=",
                ">",
                "<",
                ">=",
                "<=",
                "contains",
                "not_contains",
                "exists",
                "not_exists",

            }:

                tokens.append(
                    Token(
                        TokenType.OPERATOR,
                        value,
                    )
                )

                continue

            if value in {

                "AND",
                "OR",
                "NOT",

            }:

                tokens.append(
                    Token(
                        TokenType.LOGIC,
                        value,
                    )
                )

                continue

            if value == "(":

                tokens.append(
                    Token(
                        TokenType.LPAREN,
                        value,
                    )
                )

                continue

            if value == ")":

                tokens.append(
                    Token(
                        TokenType.RPAREN,
                        value,
                    )
                )

                continue

            if value == ",":

                tokens.append(
                    Token(
                        TokenType.COMMA,
                        value,
                    )
                )

                continue

            if value.startswith('"'):

                tokens.append(
                    Token(
                        TokenType.STRING,
                        value[1:-1],
                    )
                )

                continue

            if value.replace(".", "", 1).isdigit():

                tokens.append(
                    Token(
                        TokenType.NUMBER,
                        value,
                    )
                )

                continue

            tokens.append(
                Token(
                    TokenType.IDENT,
                    value,
                )
            )

        tokens.append(
            Token(
                TokenType.EOF,
                "",
            )
        )

        return tokens
