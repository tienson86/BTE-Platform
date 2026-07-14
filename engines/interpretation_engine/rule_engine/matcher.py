"""
matcher.py
==========

Rule Matcher.

Nhiệm vụ
--------
- Nhận Rule
- Parse Condition -> AST
- Đánh giá AST
- Trả về True / False

Matcher không biết chi tiết các Operator.
"""

from __future__ import annotations

from typing import Iterable, List

from .condition_parser import ConditionParser
from .evaluator import Evaluator
from .registry import OperatorRegistry

from ..models.context import InterpretationContext
from ..models.rule import Rule
from ..models.rule_result import RuleResult


class RuleMatcher:
    """
    Rule Matcher.
    """

    def __init__(
        self,
        registry: OperatorRegistry | None = None,
    ) -> None:

        self.registry = registry or OperatorRegistry()

        if self.registry.count == 0:
            self.registry.load_builtin()

        self.parser = ConditionParser()

        self.evaluator = Evaluator(
            self.registry,
        )

    # =====================================================
    # Match One Rule
    # =====================================================

    def match(
        self,
        context: InterpretationContext,
        rule: Rule,
    ) -> RuleResult:

        # Rule không có điều kiện
        if not rule.condition:

            return RuleResult(
                rule=rule,
                matched=True,
                priority=rule.priority,
                score=rule.weight,
                text=rule.result,
            )

        ast = self.parser.parse(
            rule.condition
        )

        matched = self.evaluator.evaluate(
            context=context,
            rule=rule,
            ast=ast,
        )

        return RuleResult(

            rule=rule,

            matched=matched,

            priority=rule.priority,

            score=rule.weight if matched else 0,

            text=rule.result if matched else "",

        )

    # =====================================================
    # Match Many Rules
    # =====================================================

    def match_all(
        self,
        context: InterpretationContext,
        rules: Iterable[Rule],
    ) -> List[RuleResult]:

        results: List[RuleResult] = []

        for rule in rules:

            results.append(

                self.match(
                    context,
                    rule,
                )

            )

        return results

    # =====================================================
    # Match & Filter
    # =====================================================

    def match_only(
        self,
        context: InterpretationContext,
        rules: Iterable[Rule],
    ) -> List[RuleResult]:

        return [

            result

            for result in self.match_all(
                context,
                rules,
            )

            if result.matched

        ]

    # =====================================================
    # Explain
    # =====================================================

    def explain(
        self,
        context: InterpretationContext,
        rule: Rule,
    ) -> dict:

        ast = self.parser.parse(
            rule.condition
        )

        matched = self.evaluator.evaluate(
            context=context,
            rule=rule,
            ast=ast,
        )

        return {

            "rule_id": rule.id,

            "condition": rule.condition,

            "matched": matched,

            "ast": ast,

        }
