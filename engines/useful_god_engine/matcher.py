"""Matcher for Useful God rules."""

from __future__ import annotations

import json
import operator
from collections.abc import Mapping
from typing import Any


_BINARY_OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}


def _unique_maximum_contains(mapping: Mapping[Any, Any], needle: Any) -> bool:
    """True when *needle* is the unique maximum numeric value in *mapping*.

    Flow rules label this ``quá thịnh``. CSV has no numeric cutoff, so the
    predicate evaluates relative dominance of the stored counts rather than
    key presence. A lone positive count is unique-max. Ties are not unique.
    """
    target_value: float | None = None
    others: list[float] = []
    for key, raw in mapping.items():
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        if key == needle or str(key) == str(needle):
            target_value = value
            continue
        others.append(value)
    if target_value is None:
        return False
    if not others:
        return target_value > 0.0
    return target_value > max(others)


class UsefulGodMatcher:
    def evaluate(self, left: Any, op: str, right: Any) -> bool:
        if op in _BINARY_OPS:
            return _BINARY_OPS[op](left, right)
        if op == "contains":
            if left is None:
                return False
            if isinstance(left, Mapping):
                return _unique_maximum_contains(left, right)
            if isinstance(left, (list, tuple, set, frozenset)):
                return right in left
            return str(right) in str(left)
        if op == "not_contains":
            if left is None:
                return True
            if isinstance(left, Mapping):
                return not _unique_maximum_contains(left, right)
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
