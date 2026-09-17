"""Temperature stage for Useful God pipeline."""

from __future__ import annotations

from typing import Any

from ..rule_state import is_rule_active


def run_temperature_stage(context: Any, rules: list[dict[str, Any]], matcher: Any) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for rule in rules:
        if not is_rule_active(rule):
            continue
        if matcher.match(context, rule):
            item = dict(rule)
            item["rule_group"] = "temperature"
            matches.append(item)
    return matches
