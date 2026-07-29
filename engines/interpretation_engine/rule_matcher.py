"""
rule_matcher.py
===============

BTE Platform
Interpretation Engine

Rule Matcher (WP4)

Pipeline:
    legacy rule row
        → RuleAdapter (Rule Contract V1)
        → RuleConditionMatcher
        → bool

Public API unchanged: ``match(context, rules)``.
"""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from engines.rule_contract import RuleAdapter, RuleConditionMatcher

from .condition_parser import ConditionParser
from .condition_evaluator import ConditionEvaluator


class RuleMatcher:
    """
    Match Rule với RuleContext.

    WP4: Adapter + Matcher V1. Legacy parser kept as fallback only.
    """

    def __init__(
        self,
        parser: ConditionParser | None = None,
        evaluator: ConditionEvaluator | None = None,
    ):
        self.parser = parser or ConditionParser()
        self.evaluator = evaluator or ConditionEvaluator()
        self.adapter = RuleAdapter()
        self.contract_matcher = RuleConditionMatcher(self.adapter)

    # =====================================================
    # Public API
    # =====================================================

    def match(
        self,
        context: Any,
        rules: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Match danh sách Rule against RuleContext."""
        if not rules:
            return []

        matched: List[Dict[str, Any]] = []
        for rule in rules:
            if not self.validate_rule(rule):
                continue
            if self.match_one(context, rule):
                matched.append(rule)

        return self.sort_by_priority(matched)

    def match_one(self, context: Any, rule: Dict[str, Any]) -> bool:
        """Match một Rule via Rule Contract V1."""
        # Unconditional
        conditions = rule.get("conditions")
        condition = rule.get("condition")
        required = rule.get("required_conditions")
        if (
            (conditions is None or conditions == [] or conditions == {})
            and not condition
            and not required
        ):
            return True

        try:
            return self.contract_matcher.match_rule(rule, context)
        except Exception:
            # Legacy fallback for old key=value condition dicts
            return self._legacy_match(context, rule)

    def match_all(
        self,
        context: Any,
        rules: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        return self.match(context=context, rules=rules)

    def _legacy_match(self, context: Any, rule: Dict[str, Any]) -> bool:
        condition = rule.get("condition")
        if not condition:
            return True
        if isinstance(condition, dict) and not any(
            isinstance(v, (list, dict)) for v in condition.values()
        ):
            # Flat equality map against context / facts
            for key, expected in condition.items():
                actual = None
                if isinstance(context, dict):
                    actual = context.get(key)
                    if actual is None:
                        facts = context.get("facts") or {}
                        if isinstance(facts, dict):
                            actual = facts.get(key)
                if str(actual) != str(expected) and actual != expected:
                    return False
            return True
        try:
            nodes = self.parser.parse(condition)
        except Exception:
            return False
        try:
            return self.evaluator.evaluate(context=context, nodes=nodes)
        except Exception:
            return False

    # =====================================================
    # Validation / filter / group / sort (unchanged API)
    # =====================================================

    @staticmethod
    def validate_rule(rule: Dict[str, Any]) -> bool:
        return isinstance(rule, dict)

    def filter_by_category(
        self,
        rules: List[Dict[str, Any]],
        category: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        if not category:
            return list(rules)
        return [rule for rule in rules if rule.get("category") == category]

    def filter_by_layer(
        self,
        rules: List[Dict[str, Any]],
        layer: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        if not layer:
            return list(rules)
        return [rule for rule in rules if rule.get("layer") == layer]

    def group_by_category(
        self,
        rules: List[Dict[str, Any]],
    ) -> Dict[str, List[Dict[str, Any]]]:
        groups: Dict[str, List[Dict[str, Any]]] = {}
        for rule in rules:
            category = rule.get("category", "default")
            groups.setdefault(category, []).append(rule)
        return groups

    def group_by_layer(
        self,
        rules: List[Dict[str, Any]],
    ) -> Dict[str, List[Dict[str, Any]]]:
        groups: Dict[str, List[Dict[str, Any]]] = {}
        for rule in rules:
            layer = rule.get("layer", "default")
            groups.setdefault(layer, []).append(rule)
        return groups

    def sort_by_priority(
        self,
        rules: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Sort by priority DESC, then confidence DESC."""
        def _key(rule: Dict[str, Any]) -> tuple[float, float]:
            try:
                priority = float(rule.get("priority", 0) or 0)
            except (TypeError, ValueError):
                priority = 0.0
            try:
                confidence = float(
                    rule.get("confidence", rule.get("score", 0)) or 0
                )
            except (TypeError, ValueError):
                confidence = 0.0
            return (priority, confidence)

        return sorted(rules, key=_key, reverse=True)

    def count(self, rules: List[Dict[str, Any]]) -> int:
        return len(rules)

    def is_empty(self, rules: List[Dict[str, Any]]) -> bool:
        return len(rules) == 0

    def first(self, rules: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        return rules[0] if rules else None

    def last(self, rules: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        return rules[-1] if rules else None
