"""Matcher for Useful God rules."""

from __future__ import annotations

import json
import operator
from typing import Any


_BINARY_OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}


class UsefulGodMatcher:
    def evaluate(self, left: Any, op: str, right: Any) -> bool:
        if op in _BINARY_OPS:
            return _BINARY_OPS[op](left, right)
        if op == "contains":
            if left is None:
                return False
            if isinstance(left, (list, tuple, set, frozenset, dict)):
                return right in left
            return str(right) in str(left)
        if op == "not_contains":
            if left is None:
                return True
            if isinstance(left, (list, tuple, set, frozenset, dict)):
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

    def parse_conditions(self, raw: Any) -> list[dict[str, Any]]:
        if raw is None:
            return []
        if isinstance(raw, list):
            return raw
        if isinstance(raw, str):
            text = raw.strip()
            if not text:
                return []
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                return []
            return parsed if isinstance(parsed, list) else []
        return []

    def match(self, context: Any, rule: dict[str, Any]) -> bool:
        conditions = self.parse_conditions(rule.get("conditions"))
        for cond in conditions:
            field = cond.get("field")
            op = cond.get("operator")
            value = cond.get("value")
            current = getattr(context, str(field), None)
            if not self.evaluate(current, str(op), value):
                return False
        return True
