"""Deterministic priority resolution."""

from __future__ import annotations

from engines.rule_engine.models import PRIORITY_LEVEL_RANK, MatchResult, RuleRecord


class PriorityResolver:
    """Order matched rules with stable deterministic ranking."""

    def resolve(self, rules: list[RuleRecord]) -> list[MatchResult]:
        """
        Sort rules by:

        1. explicit priority level (desc)
        2. specificity / condition count (desc)
        3. explicit priority order (desc)
        4. rule id (asc) for stable conflict resolution
        """
        ordered = sorted(
            rules,
            key=lambda rule: (
                -PRIORITY_LEVEL_RANK.get(rule.priority_level.lower(), 50),
                -rule.specificity,
                -int(rule.priority_order),
                rule.id.lower(),
            ),
        )
        return [
            MatchResult(rule=rule, rank=index + 1, matched=True)
            for index, rule in enumerate(ordered)
        ]
