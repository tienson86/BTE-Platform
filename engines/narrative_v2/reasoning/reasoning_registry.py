"""Reasoning rule registry. Registration order is the priority fallback."""

from __future__ import annotations

from engines.narrative_v2.reasoning.reasoning_rules import (
    APPROVED_RULES,
    CATALOG_CONTRACT_GAPS,
    ReasoningRule,
)
from engines.narrative_v2.reasoning.reasoning_context import ReasoningContractGap


class ReasoningRegistry:
    """Approved-rule catalog. Does not invent relationships."""

    def __init__(self, rules: tuple[ReasoningRule, ...] | None = None) -> None:
        self._rules = rules if rules is not None else APPROVED_RULES
        self._by_id = {rule.rule_id: rule for rule in self._rules}

    def rules(self) -> tuple[ReasoningRule, ...]:
        """Return rules in stable registration order."""
        return self._rules

    def get(self, rule_id: str) -> ReasoningRule | None:
        """Return a registered rule or None. Does not invent."""
        return self._by_id.get(rule_id)

    def contains(self, rule_id: str) -> bool:
        """True when rule_id is registered."""
        return rule_id in self._by_id

    def catalog_gaps(self) -> tuple[ReasoningContractGap, ...]:
        """Return out-of-scope reasoning gaps. Not fired as rules."""
        return CATALOG_CONTRACT_GAPS

    def registration_index(self, rule_id: str) -> int:
        """Stable fallback order when priorities tie."""
        for index, rule in enumerate(self._rules):
            if rule.rule_id == rule_id:
                return index
        return len(self._rules)
