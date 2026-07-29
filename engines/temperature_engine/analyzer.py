"""Temperature analyzer pipeline."""

from __future__ import annotations

from typing import Any

from .calculators.balance import run_balance_stage
from .calculators.climate import run_climate_stage
from .calculators.dryness import run_dryness_stage
from .calculators.flow import run_flow_stage
from .calculators.humidity import run_humidity_stage
from .calculators.season_temperature import run_season_stage
from .calculators.special_case import run_special_case_stage


class TemperatureAnalyzer:
    """Run temperature analysis stages."""

    def __init__(self, matcher: Any) -> None:
        self.matcher = matcher

    def analyze_primary(
        self,
        context: Any,
        grouped_rules: dict[str, list[dict[str, Any]]],
    ) -> dict[str, Any]:
        """Run stages that do not require pre-computed component scores."""
        season_matches = run_season_stage(context, grouped_rules.get("season", []), self.matcher)
        climate_matches = run_climate_stage(context, grouped_rules.get("climate", []), self.matcher)
        dryness_matches = run_dryness_stage(context, grouped_rules.get("dryness", []), self.matcher)
        humidity_matches = run_humidity_stage(context, grouped_rules.get("humidity", []), self.matcher)
        special_matches = run_special_case_stage(context, grouped_rules.get("special", []), self.matcher)
        flow_matches = run_flow_stage(context, grouped_rules.get("flow", []), self.matcher)

        return {
            "season_matches": season_matches,
            "climate_matches": climate_matches,
            "dryness_matches": dryness_matches,
            "humidity_matches": humidity_matches,
            "special_matches": special_matches,
            "flow_matches": flow_matches,
        }

    def analyze_balance(
        self,
        context: Any,
        grouped_rules: dict[str, list[dict[str, Any]]],
    ) -> list[dict[str, Any]]:
        """Run balance stage after component scores are on context."""
        return run_balance_stage(context, grouped_rules.get("balance", []), self.matcher)
