"""Strength analyzer pipeline."""

from __future__ import annotations

from typing import Any

from .calculators.combination_strength import run_combination_stage
from .calculators.control_strength import run_control_stage
from .calculators.drain_strength import run_drain_stage
from .calculators.root_strength import run_root_stage
from .calculators.season_strength import run_season_stage
from .calculators.special_case import run_special_case_stage
from .calculators.support_strength import run_support_stage


class StrengthAnalyzer:
    """Run all strength analysis stages."""

    def __init__(self, matcher: Any) -> None:
        self.matcher = matcher

    def analyze(
        self,
        context: Any,
        grouped_rules: dict[str, list[dict[str, Any]]],
    ) -> dict[str, Any]:
        """Run stage pipeline and return matched rules per group."""
        season_matches = run_season_stage(
            context,
            grouped_rules.get("season", []),
            self.matcher,
        )
        root_matches = run_root_stage(
            context,
            grouped_rules.get("root", []),
            self.matcher,
        )
        support_matches = run_support_stage(
            context,
            grouped_rules.get("support", []),
            self.matcher,
        )
        control_matches = run_control_stage(
            context,
            grouped_rules.get("control", []),
            self.matcher,
        )
        drain_matches = run_drain_stage(
            context,
            grouped_rules.get("drain", []),
            self.matcher,
        )
        combination_matches = run_combination_stage(
            context,
            grouped_rules.get("combination", []),
            self.matcher,
        )
        special_matches = run_special_case_stage(
            context,
            grouped_rules.get("special", []),
            self.matcher,
        )

        all_matches = (
            season_matches
            + root_matches
            + support_matches
            + control_matches
            + drain_matches
            + combination_matches
            + special_matches
        )

        return {
            "season_matches": season_matches,
            "root_matches": root_matches,
            "support_matches": support_matches,
            "control_matches": control_matches,
            "drain_matches": drain_matches,
            "combination_matches": combination_matches,
            "special_matches": special_matches,
            "all_matches": all_matches,
        }
