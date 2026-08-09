"""Seasonal Core knowledge-package integration stage."""

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

SEASONAL_CHART_KEYS: tuple[str, ...] = (
    "month_branch",
    "season",
    "season_phase",
    "season_score",
    "lunar_month_index",
)


class SeasonalStage:
    """Bind Seasonal Core. Does not reclassify month command."""

    stage_id: str = "seasonal"
    name: str = "Seasonal"
    version: str = "1.0.0"
    order: int = 30
    package_id: str = "bz_02_seasonal_core"

    def dependencies(self) -> tuple[str, ...]:
        """Seasonal consumes Four Pillars facts."""
        return ("four_pillars",)

    def execute(
        self,
        context: AnalysisExecutionContext,
        package: LoadedPackage,
    ) -> Mapping[str, Any]:
        """Publish Seasonal binding and pass through existing season facts."""
        require_upstream(context, self.stage_id, self.dependencies())
        payload = bind_package_payload(
            stage_id=self.stage_id,
            package=package,
            produced_signals=("season", "season_phase", "season_score"),
            consumed_signals=("month_branch", "lunar_month_index"),
            chart_facts=chart_subset(context.chart, SEASONAL_CHART_KEYS),
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
            messages=("seasonal_package_bound",),
        )
