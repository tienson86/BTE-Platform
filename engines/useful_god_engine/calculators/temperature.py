"""Temperature stage for Useful God pipeline."""

from __future__ import annotations

from typing import Any


def run_temperature_stage(context: Any, rules: list[dict[str, Any]], matcher: Any) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for rule in rules:
        if str(rule.get("status") or "active") != "active":
            continue
        if matcher.match(context, rule):
            item = dict(rule)
            item["rule_group"] = "temperature"
            matches.append(item)
    return matches
