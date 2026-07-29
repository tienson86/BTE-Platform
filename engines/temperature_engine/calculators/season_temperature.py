"""Season temperature stage."""

from __future__ import annotations

from typing import Any

from . import run_rule_stage


def run_season_stage(context: Any, rules: list[dict[str, Any]], matcher: Any) -> list[dict[str, Any]]:
    """Match season temperature rules."""
    return run_rule_stage(context, rules, matcher, "season")
