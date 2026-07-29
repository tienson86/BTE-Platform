"""Priority resolution from 05_priority_rules.csv."""

from __future__ import annotations

import json
from typing import Any


class PriorityResolver:
    """Resolve winner candidate using group-priority + candidate score."""

    def __init__(self, priority_rules: list[dict[str, Any]]):
        self._map: dict[str, int] = {}
        for row in priority_rules:
            conditions = self._parse_conditions(row.get("conditions"))
            for cond in conditions:
                if cond.get("field") == "rule_group" and cond.get("operator") == "==":
                    self._map[str(cond.get("value"))] = int(row.get("priority") or 0)
        self._map.setdefault("special", 100)
        self._map.setdefault("season", 90)
        self._map.setdefault("strength", 80)
        self._map.setdefault("temperature", 70)
        self._map.setdefault("flow", 60)

    def resolve(self, candidates: list[dict[str, Any]]) -> dict[str, Any] | None:
        if not candidates:
            return None

        def key_fn(item: dict[str, Any]) -> tuple[int, float, int]:
            group = str(item.get("rule_group") or "")
            group_priority = int(self._map.get(group, 0))
            score = float(item.get("score") or 0.0)
            rule_priority = int(item.get("priority") or 0)
            return (group_priority, score, rule_priority)

        return max(candidates, key=key_fn)

    @staticmethod
    def _parse_conditions(raw: Any) -> list[dict[str, Any]]:
        if isinstance(raw, list):
            return raw
        if isinstance(raw, str):
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                return []
            return parsed if isinstance(parsed, list) else []
        return []
