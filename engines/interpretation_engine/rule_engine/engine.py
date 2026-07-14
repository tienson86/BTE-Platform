"""
engine.py
=========

Rule Engine

Đây là API chính của Rule Engine.

Pipeline:

RuleLoader
    ↓
RuleMatcher
    ↓
ConflictResolver
    ↓
PrioritySorter
    ↓
RuleResult
"""

from __future__ import annotations

from typing import Iterable, List, Optional

from ..models.context import InterpretationContext
from ..models.rule import Rule
from ..models.rule_result import RuleResult

from .matcher import RuleMatcher
from .registry import OperatorRegistry


class RuleEngine:
    """
    Rule Engine.

    Chịu trách nhiệm điều phối toàn bộ quá trình
    đánh giá Rule.
    """

    def __init__(
        self,
        matcher: RuleMatcher | None = None,
        registry: OperatorRegistry | None = None,
    ) -> None:

        self.registry = registry or OperatorRegistry()

        if self.registry.count == 0:
            self.registry.load_builtin()

        self.matcher = matcher or RuleMatcher(
            registry=self.registry,
        )

    # =====================================================
    # Run
    # =====================================================

    def run(
        self,
        context: InterpretationContext,
        rules: Iterable[Rule],
    ) -> List[RuleResult]:
        """
        Chạy toàn bộ Rule.
        """

        results = self.matcher.match_all(
            context=context,
            rules=rules,
        )

        return self.sort(results)

    # =====================================================
    # Run matched only
    # =====================================================

    def run_matched(
        self,
        context: InterpretationContext,
        rules: Iterable[Rule],
    ) -> List[RuleResult]:
        """
        Chỉ lấy Rule khớp.
        """

        results = self.matcher.match_only(
            context=context,
            rules=rules,
        )

        return self.sort(results)

    # =====================================================
    # Run one
    # =====================================================

    def run_one(
        self,
        context: InterpretationContext,
        rule: Rule,
    ) -> RuleResult:

        return self.matcher.match(
            context=context,
            rule=rule,
        )

    # =====================================================
    # Explain
    # =====================================================

    def explain(
        self,
        context: InterpretationContext,
        rule: Rule,
    ) -> dict:

        return self.matcher.explain(
            context=context,
            rule=rule,
        )

    # =====================================================
    # Sort
    # =====================================================

    def sort(
        self,
        results: List[RuleResult],
    ) -> List[RuleResult]:
        """
        Sắp xếp theo:
        1. Priority giảm dần
        2. Score giảm dần
        """

        return sorted(
            results,
            key=lambda r: (
                r.priority,
                r.score,
            ),
            reverse=True,
        )

    # =====================================================
    # Filter
    # =====================================================

    def filter(
        self,
        results: Iterable[RuleResult],
        *,
        matched: Optional[bool] = None,
    ) -> List[RuleResult]:

        items = list(results)

        if matched is None:
            return items

        return [
            r
            for r in items
            if r.matched == matched
        ]
