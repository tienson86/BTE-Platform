"""Rule matching infrastructure."""

from __future__ import annotations

from typing import Any, Mapping

from engines.rule_contract.matcher import RuleConditionMatcher
from engines.rule_engine.models import MatchResult, RuleRecord
from engines.rule_engine.priority import PriorityResolver

_OPERATOR_ALIASES: dict[str, str] = {
    "equals": "eq",
    "equal": "eq",
    "eq": "eq",
    "==": "eq",
    "=": "eq",
    "not_equals": "neq",
    "not_equal": "neq",
    "neq": "neq",
    "!=": "neq",
    "greater_than": "gt",
    "gt": "gt",
    ">": "gt",
    "greater_or_equal": "gte",
    "gte": "gte",
    ">=": "gte",
    "less_than": "lt",
    "lt": "lt",
    "<": "lt",
    "less_or_equal": "lte",
    "lte": "lte",
    "<=": "lte",
    "in": "in",
    "not_in": "not_in",
    "contains": "contains",
    "contains_any": "contains_any",
    "contains_all": "contains_all",
    "exists": "exists",
    "not_exists": "not_exists",
    "between": "between",
}


class RuleMatcher:
    """
    Match loaded rules against a context.

    Reuses Rule Contract V1 evaluation for exact, conditional, and composite
    conditions without changing analytical knowledge.
    """

    def __init__(
        self,
        condition_matcher: RuleConditionMatcher | None = None,
        priority_resolver: PriorityResolver | None = None,
    ) -> None:
        self._condition_matcher = condition_matcher or RuleConditionMatcher()
        self._priority_resolver = priority_resolver or PriorityResolver()

    def match(
        self,
        rules: list[RuleRecord],
        context: Mapping[str, Any] | Any,
        *,
        resolve_priority: bool = True,
    ) -> list[MatchResult]:
        """Return all matching rule candidates, optionally priority-ordered."""
        matched: list[RuleRecord] = []
        for rule in rules:
            if self.match_one(rule, context):
                matched.append(rule)
        if not resolve_priority:
            return [
                MatchResult(rule=rule, rank=index + 1, matched=True)
                for index, rule in enumerate(matched)
            ]
        return self._priority_resolver.resolve(matched)

    def match_one(self, rule: RuleRecord, context: Mapping[str, Any] | Any) -> bool:
        """Evaluate one rule against context."""
        if not rule.conditions:
            return True
        adapted = self._to_match_payload(rule)
        return self._condition_matcher.match_rule(adapted, context)

    def match_exact(
        self,
        rules: list[RuleRecord],
        context: Mapping[str, Any] | Any,
    ) -> list[MatchResult]:
        """Match rules that use only equality predicates."""
        exact_rules = [
            rule
            for rule in rules
            if rule.conditions
            and all(self._is_exact_condition(item) for item in rule.conditions)
        ]
        return self.match(exact_rules, context)

    def match_conditional(
        self,
        rules: list[RuleRecord],
        context: Mapping[str, Any] | Any,
    ) -> list[MatchResult]:
        """Match rules that include at least one non-equality condition."""
        conditional_rules = [
            rule
            for rule in rules
            if rule.conditions
            and any(not self._is_exact_condition(item) for item in rule.conditions)
        ]
        return self.match(conditional_rules, context)

    def _to_match_payload(self, rule: RuleRecord) -> dict[str, Any]:
        """Normalize RULE_MODEL / V1 conditions into adapter-friendly payload."""
        conditions: list[dict[str, Any]] = []
        for index, item in enumerate(rule.conditions):
            field = item.get("field") or item.get("path") or item.get("type")
            operator = item.get("operator") or "eq"
            normalized_operator = _OPERATOR_ALIASES.get(
                str(operator).strip().lower(),
                str(operator).strip().lower(),
            )
            conditions.append(
                {
                    "condition_id": str(item.get("condition_id") or f"{rule.id}:{index}"),
                    "field": str(field or ""),
                    "operator": normalized_operator,
                    "value": item.get("value"),
                }
            )
        return {
            "id": rule.id,
            "condition_group": rule.condition_group,
            "conditions": conditions,
        }

    @staticmethod
    def _is_exact_condition(item: Mapping[str, Any]) -> bool:
        """Return True when condition is an equality check."""
        operator = str(item.get("operator") or "eq").strip().lower()
        normalized = _OPERATOR_ALIASES.get(operator, operator)
        return normalized == "eq"
