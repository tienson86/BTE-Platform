"""Shared stage runner for temperature calculators."""

from __future__ import annotations

from typing import Any


def run_rule_stage(
    context: Any,
    rules: list[dict[str, Any]],
    matcher: Any,
    rule_group: str,
) -> list[dict[str, Any]]:
    """Match active rules for a pipeline stage."""
    matches: list[dict[str, Any]] = []
    for rule in rules:
        if not matcher.is_active(rule):
            continue
        target = str(rule.get("score_target") or rule_group)
        if target in {"level", "config", "priority"}:
            continue
        if not matcher.match(context, rule):
            continue
        item = dict(rule)
        item["rule_group"] = rule_group
        matches.append(item)
    return matches
