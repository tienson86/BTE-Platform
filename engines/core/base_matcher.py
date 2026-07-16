"""
Base Matcher.

Framework so khớp Rule.
"""

from __future__ import annotations

from abc import ABC
import operator


OPERATORS = {

    "==": operator.eq,

    "!=": operator.ne,

    ">": operator.gt,

    ">=": operator.ge,

    "<": operator.lt,

    "<=": operator.le,

    "in": lambda a, b: a in b,

    "contains": lambda a, b: b in a,

}


class BaseMatcher(ABC):

    def evaluate(
        self,
        left,
        op: str,
        right
    ) -> bool:

        if op not in OPERATORS:

            raise ValueError(
                f"Unsupported operator: {op}"
            )

        return OPERATORS[op](left, right)

    def match(
        self,
        context,
        conditions
    ) -> bool:

        for cond in conditions:

            field = cond["field"]

            op = cond["operator"]

            value = cond["value"]

            current = getattr(
                context,
                field,
                None
            )

            if not self.evaluate(
                current,
                op,
                value
            ):
                return False

        return True
