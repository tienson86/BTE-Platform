"""Priority resolution for Temperature Engine."""

from __future__ import annotations

import json
from typing import Any


class TemperaturePriorityResolver:
    """Resolve level and group priority from database rules."""

    def __init__(self, priority_rules: list[dict[str, Any]]) -> None:
        self._group_map: dict[str, int] = {}
        for row in priority_rules:
            target = str(row.get("score_target") or "")
            if target == "level":
                continue
            conditions = self._parse_conditions(row.get("conditions"))
            for cond in conditions:
                if cond.get("field") == "rule_group" and cond.get("operator") == "==":
                    self._group_map[str(cond.get("value"))] = int(row.get("priority") or 0)
        self._group_map.setdefault("special", 100)
        self._group_map.setdefault("climate", 95)
        self._group_map.setdefault("season", 90)
        self._group_map.setdefault("dryness", 85)
        self._group_map.setdefault("humidity", 85)
        self._group_map.setdefault("flow", 80)
        self._group_map.setdefault("balance", 75)

    def resolve_level(
        self,
        context: Any,
        level_rules: list[dict[str, Any]],
        matcher: Any,
    ) -> dict[str, Any] | None:
        """Pick winning level rule after temperature_score is computed."""
        candidates: list[dict[str, Any]] = []
        for rule in level_rules:
            if not matcher.is_active(rule):
                continue
            if not matcher.match(context, rule):
                continue
            candidates.append(rule)
        if not candidates:
            return None

        def key_fn(item: dict[str, Any]) -> tuple[int, int]:
            return (int(item.get("priority") or 0), int(item.get("score") or 0))

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
