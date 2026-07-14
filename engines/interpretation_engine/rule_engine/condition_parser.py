"""
condition_parser.py
===================

Recursive Descent Parser cho Rule Engine.

Grammar (V1.0)
--------------

expression
    := or_expression

or_expression
    := and_expression (OR and_expression)*

and_expression
    := unary_expression (AND unary_expression)*

unary_expression
    := NOT unary_expression
     | primary

primary
    := "(" expression ")"
     | function
     | condition

condition
    := IDENT OPERATOR VALUE

function
    := IDENT "(" IDENT? ")"
"""

from __future__ import annotations

from typing import List

from .ast import (
    ASTNode,
    BinaryNode,
    ConditionNode,
    FunctionNode,
    Logic,
    Operator,
    UnaryNode,
)

from .tokenizer import (
    Token,
    TokenType,
    Tokenizer,
)


class ConditionParser:
    """
    Recursive Descent Parser.
    """

    def __init__(self):

        self.tokens: List[Token] = []

        self.pos = 0

    # =====================================================
    # Public API
    # =====================================================

    def parse(
        self,
        text: str,
    ) -> ASTNode:

        tokenizer = Tokenizer()

        self.tokens = tokenizer.tokenize(text)

        self.pos = 0

        return self.expression()

    # =====================================================
    # Grammar
    # =====================================================

    def expression(self):

        return self.or_expression()

    # -----------------------------------------------------

    def or_expression(self):

        node = self.and_expression()

        while self.match(
            TokenType.LOGIC,
            "OR",
        ):

            right = self.and_expression()

            node = BinaryNode(
                left=node,
                operator=Logic.OR,
                right=right,
            )

        return node

    # -----------------------------------------------------

    def and_expression(self):

        node = self.unary_expression()

        while self.match(
            TokenType.LOGIC,
            "AND",
        ):

            right = self.unary_expression()

            node = BinaryNode(
                left=node,
                operator=Logic.AND,
                right=right,
            )

        return node

    # -----------------------------------------------------

    def unary_expression(self):

        if self.match(
            TokenType.LOGIC,
            "NOT",
        ):

            return UnaryNode(
                operator=Logic.NOT,
                operand=self.unary_expression(),
            )

        return self.primary()

    # -----------------------------------------------------

    def primary(self):

        token = self.peek()

        # (...)

        if token.type == TokenType.LPAREN:

            self.consume()

            node = self.expression()

            self.expect(TokenType.RPAREN)

            return node

        # Function

        if self.is_function():

            return self.function()

        # Condition

        return self.condition()

    # =====================================================
    # Function
    # =====================================================

    def function(self):

        name = self.expect(
            TokenType.IDENT
        ).value

        self.expect(
            TokenType.LPAREN
        )

        argument = None

        if self.peek().type != TokenType.RPAREN:

            argument = self.consume().value

        self.expect(
            TokenType.RPAREN
        )

        return FunctionNode(

            name=name,

            argument=argument,

        )

    # =====================================================
    # Condition
    # =====================================================

    def condition(self):

        field = self.expect(
            TokenType.IDENT
        ).value

        operator = self.expect(
            TokenType.OPERATOR
        ).value

        value = self.consume().value

        return ConditionNode(

            field=field,

            operator=Operator(operator),

            value=value,

        )

    # =====================================================
    # Helper
    # =====================================================

    def is_function(self):

        if self.peek().type != TokenType.IDENT:

            return False

        if self.pos + 1 >= len(self.tokens):

            return False

        return (

            self.tokens[self.pos + 1].type

            == TokenType.LPAREN

        )

    # -----------------------------------------------------

    def peek(self):

        return self.tokens[self.pos]

    def consume(self):

        token = self.tokens[self.pos]

        self.pos += 1

        return token

    def expect(self, token_type):

        token = self.consume()

        if token.type != token_type:

            raise SyntaxError(

                f"Expected {token_type}, "

                f"got {token.type}"

            )

        return token

    def match(
        self,
        token_type,
        value=None,
    ):

        token = self.peek()

        if token.type != token_type:

            return False

        if value is not None:

            if token.value != value:

                return False

        self.consume()

        return True
