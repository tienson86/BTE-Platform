"""Useful God analyzer pipeline."""

from __future__ import annotations

from typing import Any

from .calculators.balance import run_balance_stage
from .calculators.flow import run_flow_stage
from .calculators.season import run_season_stage
from .calculators.special_case import run_special_case_stage
from .calculators.strength import run_strength_stage
from .calculators.temperature import run_temperature_stage


class UsefulGodAnalyzer:
    """Run all six analysis stages and generate candidates."""

    def __init__(self, matcher: Any):
        self.matcher = matcher

    def analyze(self, context: Any, grouped_rules: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
        """Run stage pipeline and return stage outputs + candidate list."""
        strength_candidates = run_strength_stage(
            context,
            grouped_rules.get("strength", []),
            self.matcher,
        )
        season_candidates = run_season_stage(
            context,
            grouped_rules.get("season", []),
            self.matcher,
        )
        temperature_candidates = run_temperature_stage(
            context,
            grouped_rules.get("temperature", []),
            self.matcher,
        )
        flow_candidates = run_flow_stage(
            context,
            grouped_rules.get("flow", []),
            self.matcher,
        )
        balance_summary = run_balance_stage(context)
        special_candidates = run_special_case_stage(
            context,
            grouped_rules.get("special", []),
            self.matcher,
        )

        candidates = (
            strength_candidates
            + season_candidates
            + temperature_candidates
            + flow_candidates
            + special_candidates
        )

        return {
            "strength_candidates": strength_candidates,
            "season_candidates": season_candidates,
            "temperature_candidates": temperature_candidates,
            "flow_candidates": flow_candidates,
            "special_candidates": special_candidates,
            "balance_summary": balance_summary,
            "candidate_list": candidates,
        }
