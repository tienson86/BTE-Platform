"""Special-case stage for Useful God pipeline."""

from __future__ import annotations

from typing import Any

from engines.pattern_engine.override_eligibility import resolve_context_override_eligible


def run_special_case_stage(context: Any, rules: list[dict[str, Any]], matcher: Any) -> list[dict[str, Any]]:
    """Match spc_* only when Pattern override eligibility is granted."""
    if not resolve_context_override_eligible(context):
        return []

    matches: list[dict[str, Any]] = []
    for rule in rules:
        if str(rule.get("status") or "active") != "active":
            continue
        if matcher.match(context, rule):
            item = dict(rule)
            item["rule_group"] = "special"
            matches.append(item)
    return matches
