"""
BTE Platform
=============================

Interpretation Engine

Conflict Resolver

Giải quyết xung đột giữa các Rule đã Match.

Author : BTE Project
Version : 1.0.0
"""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable
from typing import Any

from .result import MatchResult


class ConflictResolver:
    """
    Conflict Resolver.

    Chức năng

    - Loại bỏ Rule xung đột
    - Chỉ giữ Rule ưu tiên cao nhất
    - Hỗ trợ Exclusive Group
    - Hỗ trợ Override
    - Hỗ trợ Replace
    - Hỗ trợ Merge
    """

    VERSION = "1.0.0"

    def __init__(self) -> None:

        self._statistics = {

            "input": 0,

            "output": 0,

            "removed": 0,

            "merged": 0,

            "override": 0,

        }

    # =====================================================
    # Public API
    # =====================================================

    def resolve(
        self,
        results: Iterable[MatchResult],
    ) -> list[MatchResult]:
        """
        Giải quyết toàn bộ xung đột.
        """

        items = list(results)

        self.reset_statistics()

        self._statistics["input"] = len(items)

        items = self._resolve_exclusive(items)

        items = self._resolve_override(items)

        items = self._resolve_replace(items)

        items = self._resolve_merge(items)

        self._statistics["output"] = len(items)

        return items

    # =====================================================
    # Exclusive
    # =====================================================

    def _resolve_exclusive(
        self,
        results: list[MatchResult],
    ) -> list[MatchResult]:

        groups = defaultdict(list)

        output = []

        for result in results:

            group = result.data.get(
                "exclusive_group"
            )

            if not group:

                output.append(result)

                continue

            groups[group].append(result)

        for values in groups.values():

            values.sort(

                key=lambda r: (
                    r.priority,
                    r.score,
                ),

                reverse=True,

            )

            output.append(values[0])

            self._statistics["removed"] += (
                len(values) - 1
            )

        return output

    # =====================================================
    # Override
    # =====================================================

    def _resolve_override(
        self,
        results: list[MatchResult],
    ) -> list[MatchResult]:

        removed = set()

        for result in results:

            targets = result.data.get(
                "override",
                [],
            )

            for target in targets:

                removed.add(target)

        output = []

        for result in results:

            if result.rule_id in removed:

                self._statistics["override"] += 1

                continue

            output.append(result)

        return output

    # =====================================================
    # Replace
    # =====================================================

    def _resolve_replace(
        self,
        results: list[MatchResult],
    ) -> list[MatchResult]:

        replace_map = {}

        output = []

        for result in results:

            target = result.data.get(
                "replace"
            )

            if target:

                replace_map[target] = result

            else:

                output.append(result)

        final = []

        for result in output:

            if result.rule_id in replace_map:

                final.append(
                    replace_map[result.rule_id]
                )

            else:

                final.append(result)

        for value in replace_map.values():

            if value not in final:

                final.append(value)

        return final

    # =====================================================
    # Merge
    # =====================================================

    def _resolve_merge(
        self,
        results: list[MatchResult],
    ) -> list[MatchResult]:

        groups = defaultdict(list)

        output = []

        for result in results:

            key = result.data.get(
                "merge_group"
            )

            if not key:

                output.append(result)

                continue

            groups[key].append(result)

        for values in groups.values():

            merged = values[0]

            merged.score = max(
                r.score
                for r in values
            )

            merged.priority = max(
                r.priority
                for r in values
            )

            self._statistics["merged"] += (
                len(values) - 1
            )

            output.append(merged)

        return output

    # =====================================================
    # Helper
    # =====================================================

    def remove_duplicates(
        self,
        results: Iterable[MatchResult],
    ) -> list[MatchResult]:

        seen = set()

        output = []

        for result in results:

            if result.rule_id in seen:

                continue

            seen.add(result.rule_id)

            output.append(result)

        return output

    # =====================================================
    # Statistics
    # =====================================================

    @property
    def statistics(self):

        return self._statistics.copy()

    def reset_statistics(self):

        self._statistics = {

            "input": 0,

            "output": 0,

            "removed": 0,

            "merged": 0,

            "override": 0,

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

    def health(self) -> dict[str, Any]:

        return {

            "version": self.VERSION,

            "statistics": self.statistics,

            "ready": True,

        }

    # =====================================================
    # Magic Methods
    # =====================================================

    def __repr__(self):

        return (

            f"<ConflictResolver "

            f"removed={self._statistics['removed']} "

            f"merged={self._statistics['merged']}>"

        )
