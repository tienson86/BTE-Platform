"""Condition matching for priority rules."""

from __future__ import annotations

import operator
import re
from collections.abc import Mapping
from typing import Any

from .exceptions import PriorityConditionError
from .models import ConditionMatch, PriorityCondition, PriorityData


class ConditionMatcher:
    """Evaluate ``priority_conditions.json`` records against a context object.

    The matcher accepts a plain dictionary so it can be called from any engine.
    Conditions can be represented as boolean fact keys, entries in a ``facts``
    collection, or simple comparison expressions such as ``strength_score >= 80``.
    """

    _EXPRESSION = re.compile(r"^([A-Za-z_][\w.]*)\s*(>=|<=|==|!=|=|>|<)\s*(.+)$")
    _OPERATORS = {
        "=": operator.eq,
        "==": operator.eq,
        "!=": operator.ne,
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le,
    }

    def __init__(self, data: PriorityData) -> None:
        self.data = data

    def match(
        self,
        context: Mapping[str, Any],
        *,
        include_unmatched: bool = False,
        rule_ids: set[str] | None = None,
    ) -> tuple[ConditionMatch, ...]:
        """Return condition matches for the supplied runtime context."""

        results: list[ConditionMatch] = []
        for condition in self.data.conditions:
            if not condition.enabled:
                continue
            if rule_ids is not None and condition.priority_rule not in rule_ids:
                continue
            result = self.evaluate(condition, context)
            if result.matched or include_unmatched:
                results.append(result)
        return tuple(results)

    def evaluate(
        self, condition: PriorityCondition, context: Mapping[str, Any]
    ) -> ConditionMatch:
        """Evaluate one priority condition."""

        matched_terms: list[str] = []
        failed_terms: list[str] = []

        for term in condition.required_conditions:
            if self._evaluate_term(term, context):
                matched_terms.append(term)
            else:
                failed_terms.append(term)

        match_type = condition.match_type.lower()
        if not condition.required_conditions:
            matched = True
        elif match_type == "all":
            matched = not failed_terms
        elif match_type in {"any", "first", "highest_score"}:
            matched = bool(matched_terms)
        else:
            raise PriorityConditionError(
                f"Unsupported match_type '{condition.match_type}' in {condition.id}."
            )

        return ConditionMatch(
            condition=condition,
            matched=matched,
            matched_terms=tuple(matched_terms),
            failed_terms=tuple(failed_terms),
        )

    def _evaluate_term(self, term: str, context: Mapping[str, Any]) -> bool:
        term = term.strip()
        if not term:
            return True

        expression = self._EXPRESSION.match(term)
        if expression:
            field, op, raw_expected = expression.groups()
            actual = self._get_value(context, field)
            expected = self._parse_literal(raw_expected)
            return self._compare(actual, op, expected)

        explicit_conditions = context.get("conditions")
        if isinstance(explicit_conditions, Mapping) and term in explicit_conditions:
            return bool(explicit_conditions[term])

        facts = context.get("facts")
        if isinstance(facts, (set, list, tuple)):
            return term in facts

        return bool(self._get_value(context, term, default=False))

    @staticmethod
    def _get_value(
        context: Mapping[str, Any], field: str, default: Any = None
    ) -> Any:
        current: Any = context
        for part in field.split("."):
            if isinstance(current, Mapping) and part in current:
                current = current[part]
            else:
                return default
        return current

    @staticmethod
    def _parse_literal(raw_value: str) -> Any:
        value = raw_value.strip().strip('"').strip("'")
        lowered = value.lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
        if lowered in {"none", "null"}:
            return None
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            return value

    def _compare(self, actual: Any, op: str, expected: Any) -> bool:
        comparator = self._OPERATORS[op]
        if actual is None and expected is not None and op not in {"=", "==", "!="}:
            return False
        try:
            return bool(comparator(actual, expected))
        except TypeError as exc:
            raise PriorityConditionError(
                f"Cannot compare values {actual!r} {op} {expected!r}."
            ) from exc
