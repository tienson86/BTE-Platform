"""Narrative rule matching against AnalysisResult facts (not Score Rule DB)."""

from __future__ import annotations

from typing import Any

from .library_loader import NarrativeLibrary
from .narrative_context import NarrativeContext


class NarrativeRuleMatcher:
    """
    Stage — Rule Matching for narrative selection.

    Matches Pack 04 narrative rules to analysis facts / evidence.
    Does not recalculate analytical scores.
    """

    def __init__(self, library: NarrativeLibrary | None = None) -> None:
        self.library = library or NarrativeLibrary()

    def match(self, context: NarrativeContext) -> list[dict[str, Any]]:
        """Return matched narrative rules (priority desc, one winner per section)."""
        rules = self.library.load_rules()
        matched: list[dict[str, Any]] = []
        for rule in rules:
            when = rule.get("when") or {"op": "always"}
            if self._evaluate(when, context):
                matched.append(dict(rule))

        # Keep highest-priority rule per section
        winners: dict[str, dict[str, Any]] = {}
        for rule in matched:
            section = str(rule.get("section") or "")
            if not section:
                continue
            current = winners.get(section)
            if current is None:
                winners[section] = rule
                continue
            if int(rule.get("priority") or 0) > int(current.get("priority") or 0):
                winners[section] = rule
        return list(winners.values())

    def _evaluate(self, when: dict[str, Any], context: NarrativeContext) -> bool:
        op = str(when.get("op") or "always").lower()
        if op == "always":
            return True
        field = str(when.get("field") or "")
        actual = context.facts.get(field)
        if op == "eq":
            return actual == when.get("value")
        if op == "in":
            values = when.get("values") or []
            return actual in values
        if op == "gte":
            try:
                return float(actual or 0) >= float(when.get("value") or 0)
            except (TypeError, ValueError):
                return False
        if op == "evidence_min":
            return len(context.evidence_ids) >= int(when.get("value") or 0)
        return False
