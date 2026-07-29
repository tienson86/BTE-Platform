"""
Score Engine Rule Matcher (compatibility facade).

WP2B-2: delegates to Rule Contract V1 Adapter + Matcher.
No eval().
"""

from __future__ import annotations

from typing import Any, Dict, List

from engines.rule_contract import RuleAdapter, RuleConditionMatcher


class RuleMatcher:
    """
    Score Engine public matcher.

    Pipeline:
        legacy rule row
            → RuleAdapter (Rule Contract V1)
            → RuleConditionMatcher
            → bool
    """

    def __init__(self) -> None:
        self.adapter = RuleAdapter()
        self.matcher = RuleConditionMatcher(self.adapter)

    def match(self, rules, context) -> List[Dict[str, Any]]:
        """Match DataFrame / list of rules against context."""
        if rules is None:
            return []

        if hasattr(rules, "iterrows"):
            matched: List[Dict[str, Any]] = []
            for _, rule in rules.iterrows():
                data = rule.to_dict()
                if self.evaluate_rule(data, context):
                    matched.append(data)
            return matched

        if isinstance(rules, list):
            result: List[Dict[str, Any]] = []
            for rule in rules:
                data = rule if isinstance(rule, dict) else dict(rule)
                if self.evaluate_rule(data, context):
                    result.append(data)
            return result

        # single rule
        ok = self.evaluate_rule(rules, context)
        return rules if ok else []  # type: ignore[return-value]

    def evaluate_rule(self, rule, context) -> bool:
        """Evaluate one rule via Rule Contract V1."""
        return self.matcher.match_rule(rule, context)

    def evaluate(self, expression_or_rule, context) -> bool:
        """
        Backward-compatible entry.

        Historically called with a condition string. Prefer evaluate_rule.
        """
        if isinstance(expression_or_rule, dict) or hasattr(
            expression_or_rule, "to_dict"
        ):
            return self.evaluate_rule(expression_or_rule, context)

        # Treat bare string as scalar condition cell
        return self.evaluate_rule({"condition": expression_or_rule}, context)
