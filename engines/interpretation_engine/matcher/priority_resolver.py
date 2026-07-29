"""
BTE Platform
=============================

Interpretation Engine

Priority Resolver

Chịu trách nhiệm sắp xếp các Rule đã Match
theo độ ưu tiên trước khi chuyển sang
Conflict Resolver.

Author : BTE Project
Version : 1.0.0
"""

from __future__ import annotations

from typing import Iterable
from typing import Any

from .result import MatchResult


class PriorityResolver:
    """
    Priority Resolver.

    Chức năng

    - Sắp xếp Rule theo Priority
    - Sắp xếp theo Score
    - Sắp xếp theo Weight
    - Giữ Stable Sort
    """

    VERSION = "1.0.0"

    def __init__(
        self,
        descending: bool = True,
    ) -> None:

        self.descending = descending

        self._statistics = {

            "resolved": 0,

            "sorted": 0,

        }

    # =====================================================
    # Public API
    # =====================================================

    def resolve(
        self,
        results: Iterable[MatchResult],
    ) -> list[MatchResult]:
        """
        Resolve Priority.
        """

        items = list(results)

        self._statistics["resolved"] += len(items)

        items.sort(
            key=self._priority_key,
            reverse=self.descending,
        )

        self._statistics["sorted"] += len(items)

        return items

    # =====================================================
    # Sort Key
    # =====================================================

    def _priority_key(
        self,
        result: MatchResult,
    ):

        return (

            result.priority,

            result.score,

            result.rule_id,

        )

    # =====================================================
    # Helper
    # =====================================================

    def top(
        self,
        results: Iterable[MatchResult],
        limit: int = 10,
    ) -> list[MatchResult]:

        return self.resolve(results)[:limit]

    def highest(
        self,
        results: Iterable[MatchResult],
    ) -> MatchResult | None:

        data = self.resolve(results)

        if not data:

            return None

        return data[0]

    # =====================================================
    # Statistics
    # =====================================================

    @property
    def statistics(self):

        return self._statistics.copy()

    def reset_statistics(self):

        self._statistics = {

            "resolved": 0,

            "sorted": 0,

        }

    # =====================================================
    # Lifecycle
    # =====================================================

    def initialize(self):

        self.reset_statistics()

    def shutdown(self):

        return None

    # =====================================================
    # Health
    # =====================================================

    def health(self):

        return {

            "version": self.VERSION,

            "statistics": self.statistics,

            "ready": True,

        }

    # =====================================================
    # Magic
    # =====================================================

    def __repr__(self):

        return (

            f"<PriorityResolver "

            f"resolved={self._statistics['resolved']}>"

        )
