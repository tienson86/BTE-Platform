"""
Expression Evaluator

AST

↓

True / False
"""

from .parser import BinaryExpression


class ExpressionEvaluator:

    def evaluate(
        self,
        node: BinaryExpression,
        context
    ) -> bool:

        left = self.resolve(
            node.left,
            context
        )

        right = self.resolve(
            node.right,
            context
        )

        op = node.operator

        if op == "==":
            return left == right

        if op == "!=":
            return left != right

        if op == ">":
            return left > right

        if op == "<":
            return left < right

        if op == ">=":
            return left >= right

        if op == "<=":
            return left <= right

        raise ValueError(
            f"Unsupported operator: {op}"
        )

    def resolve(
        self,
        value,
        context
    ):

        #
        # Context Variable
        #

        if hasattr(context, value):

            return getattr(
                context,
                value
            )

        #
        # Integer
        #

        try:

            return int(value)

        except ValueError:

            pass

        #
        # Float
        #

        try:

            return float(value)

        except ValueError:

            pass

        #
        # Boolean
        #

        if value.lower() == "true":
            return True

        if value.lower() == "false":
            return False

        #
        # String
        #

        return value
