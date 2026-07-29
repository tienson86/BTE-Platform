"""Special case strength stage."""

from __future__ import annotations

from typing import Any

from . import run_rule_stage


def run_special_case_stage(
    context: Any,
    rules: list[dict[str, Any]],
    matcher: Any,
) -> list[dict[str, Any]]:
    """Match special-case override rules."""
    filtered = [
        r for r in rules
        if str(r.get("score_target") or "special") == "special"
    ]
    return run_rule_stage(context, filtered, matcher, "special")
