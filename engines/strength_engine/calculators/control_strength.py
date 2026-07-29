"""Control strength stage."""

from __future__ import annotations

from typing import Any

from . import run_rule_stage


def run_control_stage(
    context: Any,
    rules: list[dict[str, Any]],
    matcher: Any,
) -> list[dict[str, Any]]:
    """Match control (khắc chế) rules."""
    return run_rule_stage(context, rules, matcher, "control")
