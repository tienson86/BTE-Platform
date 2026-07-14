"""
scorer.py
=========

Rule Scorer

Chịu trách nhiệm tính điểm và sắp xếp RuleResult.
"""

from __future__ import annotations

from typing import Iterable

from ..models.rule import Rule
from ..models.rule_result import RuleResult


class RuleScorer:
    """
    Bộ chấm điểm Rule.
    """

    def __init__(
        self,
        priority_weight: float = 1.0,
        confidence_weight: float = 10.0,
        category_weight: float = 0.0,
    ) -> None:

        self.priority_weight = priority_weight
        self.confidence_weight = confidence_weight
        self.category_weight = category_weight

    # ======================================================
    # Score
    # ======================================================

    def score(
        self,
        result: RuleResult,
    ) -> float:
        """
        Tính điểm cho một RuleResult.
        """

        rule = result.rule

        score = 0.0

        # Priority
        score += getattr(rule, "priority", 0) * self.priority_weight

        # Confidence
        score += result.confidence * self.confidence_weight

        # Có thể mở rộng theo category/topic sau này

        result.score = score

        return score

    # ======================================================
    # Score Many
    # ======================================================

    def score_all(
        self,
        results: Iterable[RuleResult],
    ) -> list[RuleResult]:

        scored = []

        for result in results:

            self.score(result)

            scored.append(result)

        return scored

    # ======================================================
    # Sort
    # ======================================================

    def sort(
        self,
        results: Iterable[RuleResult],
        reverse: bool = True,
    ) -> list[RuleResult]:
        """
        Sắp xếp theo điểm giảm dần.
        """

        return sorted(
            results,
            key=lambda r: r.score,
            reverse=reverse,
        )

    # ======================================================
    # Score + Sort
    # ======================================================

    def rank(
        self,
        results: Iterable[RuleResult],
    ) -> list[RuleResult]:
        """
        Chấm điểm và sắp xếp.
        """

        scored = self.score_all(results)

        return self.sort(scored)

    # ======================================================
    # Best Result
    # ======================================================

    def best(
        self,
        results: Iterable[RuleResult],
    ) -> RuleResult | None:

        ranked = self.rank(results)

        if not ranked:
            return None

        return ranked[0]
