"""Root strength stage."""

from __future__ import annotations

from typing import Any

from . import run_rule_stage


def run_root_stage(
    context: Any,
    rules: list[dict[str, Any]],
    matcher: Any,
) -> list[dict[str, Any]]:
    """Match root (通根) rules."""
    return run_rule_stage(context, rules, matcher, "root")
