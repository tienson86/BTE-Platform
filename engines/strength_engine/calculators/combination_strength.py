"""Combination strength stage."""

from __future__ import annotations

from typing import Any

from . import run_rule_stage


def run_combination_stage(
    context: Any,
    rules: list[dict[str, Any]],
    matcher: Any,
) -> list[dict[str, Any]]:
    """Match combination (hợp hóa) rules."""
    return run_rule_stage(context, rules, matcher, "combination")
