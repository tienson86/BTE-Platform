"""Temperature Core knowledge-package integration stage."""

from __future__ import annotations

from typing import Any, Mapping

from engines.analysis_engine.integration.base_stage import (
    bind_package_payload,
    chart_subset,
    require_upstream,
)
from engines.analysis_engine.pipeline.execution_context import AnalysisExecutionContext
from engines.analysis_engine.pipeline.package_loader import LoadedPackage
from engines.analysis_engine.pipeline.pipeline_result import StageOutcome

TEMPERATURE_CHART_KEYS: tuple[str, ...] = (
    "season",
    "season_phase",
    "day_master_element",
    "climate_type",
    "temperature_score",
    "temperature_level",
    "dryness_level",
    "humidity_level",
)


class TemperatureStage:
    """Bind Temperature Core. Consumes Seasonal and Strength signals only."""

    stage_id: str = "temperature"
    name: str = "Temperature"
    version: str = "1.0.0"
    order: int = 50
    package_id: str = "bz_03_temperature_core"

    def dependencies(self) -> tuple[str, ...]:
        """Temperature consumes Seasonal and Strength outputs."""
        return ("seasonal", "strength")

    def execute(
        self,
        context: AnalysisExecutionContext,
        package: LoadedPackage,
    ) -> Mapping[str, Any]:
        """Publish Temperature binding after Seasonal and Strength."""
        require_upstream(context, self.stage_id, self.dependencies())
        payload = bind_package_payload(
            stage_id=self.stage_id,
            package=package,
            produced_signals=(
                "temperature_score",
                "temperature_level",
                "dryness_level",
                "humidity_level",
            ),
            consumed_signals=(
                "season",
                "season_phase",
                "strength_level",
                "day_master_element",
            ),
            chart_facts=chart_subset(context.chart, TEMPERATURE_CHART_KEYS),
            upstream_stages=self.dependencies(),
        )
        context.publish(self.stage_id, payload)
        return payload

    def as_outcome(self, payload: Mapping[str, Any]) -> StageOutcome:
        """Adapt the payload to the orchestration StageOutcome contract."""
        return StageOutcome(
            stage_id=self.stage_id,
            success=True,
            payload=dict(payload),
            messages=("temperature_package_bound",),
        )
