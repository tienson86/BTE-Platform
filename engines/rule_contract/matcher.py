"""
Rule Condition Matcher V1.

Evaluates RuleContract against RuleContext.

No eval(). No Python expression execution.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence

from .adapter import RuleAdapter
from .models import (
    OPERATORS_V1,
    ConditionPredicate,
    RuleContract,
    normalize_context,
    resolve_path,
)


class RuleConditionMatcher:
    """
    Match RuleContract + RuleContext → bool.
    """

    def __init__(self, adapter: RuleAdapter | None = None) -> None:
        self.adapter = adapter or RuleAdapter()

    def match_contract(
        self,
        contract: RuleContract,
        context: Any,
    ) -> bool:
        """Evaluate a V1 contract."""
        ctx = normalize_context(context)

        if contract.is_unconditional:
            return True

        group = (contract.condition_group or "AND").upper()
        results = [
            self._match_predicate(predicate, ctx)
            for predicate in contract.conditions
        ]

        if group == "OR":
            return any(results)
        # Default AND
        return all(results)

    def match_rule(self, rule: Mapping[str, Any] | Any, context: Any) -> bool:
        """Adapt legacy rule then evaluate."""
        contract = self.adapter.adapt(rule)
        return self.match_contract(contract, context)

    def match_rules(
        self,
        rules: Iterable[Any],
        context: Any,
    ) -> list[Any]:
        """
        Return legacy rules that match context.

        Preserves original rule objects/dicts for Score Engine compatibility.
        """
        matched: list[Any] = []
        for rule in rules:
            if self.match_rule(rule, context):
                matched.append(rule)
        return matched

    # =========================================================
    # Predicate evaluation
    # =========================================================

    def _match_predicate(
        self,
        predicate: ConditionPredicate,
        context: Mapping[str, Any],
    ) -> bool:
        operator = predicate.normalized_operator()
        if operator not in OPERATORS_V1:
            raise ValueError(f"Unsupported operator: {operator}")

        field = predicate.field
        expected = predicate.value

        if operator == "exists":
            return resolve_path(context, field, default=None) is not None

        if operator == "not_exists":
            return resolve_path(context, field, default=None) is None

        actual = resolve_path(context, field, default=None)

        if operator == "eq":
            return self._equals(actual, expected)

        if operator == "neq":
            return not self._equals(actual, expected)

        if operator in {"gt", "gte", "lt", "lte"}:
            return self._compare_numbers(actual, operator, expected)

        if operator == "in":
            if expected is None:
                return False
            collection = expected if isinstance(expected, (list, tuple, set)) else [expected]
            return any(self._equals(actual, item) for item in collection)

        if operator == "not_in":
            if expected is None:
                return True
            collection = expected if isinstance(expected, (list, tuple, set)) else [expected]
            return all(not self._equals(actual, item) for item in collection)

        if operator == "contains":
            return self._contains(actual, expected)

        if operator == "contains_any":
            items = expected if isinstance(expected, (list, tuple, set)) else [expected]
            return any(self._contains(actual, item) for item in items)

        if operator == "contains_all":
            items = expected if isinstance(expected, (list, tuple, set)) else [expected]
            return all(self._contains(actual, item) for item in items)

        if operator == "between":
            return self._between(actual, expected)

        return False

    @staticmethod
    def _equals(actual: Any, expected: Any) -> bool:
        if actual is None and expected is None:
            return True
        if isinstance(actual, bool) or isinstance(expected, bool):
            return bool(actual) is bool(expected) and actual == expected
        # numeric soft compare
        try:
            if isinstance(actual, (int, float)) or isinstance(expected, (int, float)):
                return float(actual) == float(expected)
        except (TypeError, ValueError):
            pass
        return str(actual) == str(expected)

    @staticmethod
    def _compare_numbers(actual: Any, operator: str, expected: Any) -> bool:
        try:
            left = float(actual)
            right = float(expected)
        except (TypeError, ValueError):
            return False
        if operator == "gt":
            return left > right
        if operator == "gte":
            return left >= right
        if operator == "lt":
            return left < right
        if operator == "lte":
            return left <= right
        return False

    @staticmethod
    def _contains(actual: Any, expected: Any) -> bool:
        if actual is None:
            return False
        if isinstance(actual, (list, tuple, set)):
            return any(
                str(item) == str(expected) or item == expected for item in actual
            )
        return str(expected) in str(actual)

    @staticmethod
    def _between(actual: Any, expected: Any) -> bool:
        if not isinstance(expected, (list, tuple)) or len(expected) != 2:
            return False
        try:
            value = float(actual)
            low = float(expected[0])
            high = float(expected[1])
        except (TypeError, ValueError):
            return False
        return low <= value <= high
