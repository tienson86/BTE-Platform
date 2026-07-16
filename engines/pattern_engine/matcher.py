"""
Pattern Matcher.
"""

import operator


OPERATORS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}


class PatternMatcher:

    def evaluate(self, left, op, right):

        if op not in OPERATORS:
            raise ValueError(f"Unsupported operator: {op}")

        return OPERATORS[op](left, right)

    def match(self, context, rule):

        conditions = rule.get("conditions", [])

        for cond in conditions:

            field = cond["field"]

            op = cond["operator"]

            value = cond["value"]

            current = getattr(context, field, None)

            if not self.evaluate(current, op, value):
                return False

        return True
