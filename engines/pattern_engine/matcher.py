"""
Pattern Matcher.

Evaluates rule conditions against a PatternContext.

Supported operators:
  ==, !=, >, >=, <, <=  — standard comparison
  contains              — value in current (list/str)
  not_contains          — value not in current (list/str)
  in                    — current in value (list)
  not_in                — current not in value (list)
"""

from __future__ import annotations

import operator
from typing import Any


_BINARY_OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">":  operator.gt,
    ">=": operator.ge,
    "<":  operator.lt,
    "<=": operator.le,
}


class PatternMatcher:

    def evaluate(self, left: Any, op: str, right: Any) -> bool:
        if op in _BINARY_OPS:
            return _BINARY_OPS[op](left, right)
        if op == "contains":
            if left is None:
                return False
            if isinstance(left, (list, tuple, set, frozenset)):
                return right in left
            return str(right) in str(left)
        if op == "not_contains":
            if left is None:
                return True
            if isinstance(left, (list, tuple, set, frozenset)):
                return right not in left
            return str(right) not in str(left)
        if op == "in":
            if not isinstance(right, (list, tuple, set, frozenset)):
                right = [right]
            return left in right
        if op == "not_in":
            if not isinstance(right, (list, tuple, set, frozenset)):
                right = [right]
            return left not in right
        raise ValueError(f"Unsupported operator: {op}")

    def match(self, context: Any, rule: dict[str, Any]) -> bool:
        """Return True when all conditions in rule match context."""
        conditions = rule.get("conditions", [])
        for cond in conditions:
            field = cond["field"]
            op = cond["operator"]
            value = cond["value"]
            current = getattr(context, field, None)
            if not self.evaluate(current, op, value):
                return False
        return True
