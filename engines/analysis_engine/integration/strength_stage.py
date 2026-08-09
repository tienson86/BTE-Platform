"""Strength Core knowledge-package integration stage."""

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

STRENGTH_CHART_KEYS: tuple[str, ...] = (
    "day_master",
    "day_master_element",
    "month_status",
    "strength_score",
    "strength_level",
)


class StrengthStage:
    """Bind Strength Core. Does not recompute strength_score."""

    stage_id: str = "strength"
    name: str = "Strength"
    version: str = "1.0.0"
    order: int = 40
    package_id: str = "bz_01_strength_core"

    def dependencies(self) -> tuple[str, ...]:
        """Strength consumes Seasonal month-command facts."""
        return ("seasonal",)

    def execute(
        self,
        context: AnalysisExecutionContext,
        package: LoadedPackage,
    ) -> Mapping[str, Any]:
        """Publish Strength binding after Seasonal has run."""
        require_upstream(context, self.stage_id, self.dependencies())
        payload = bind_package_payload(
            stage_id=self.stage_id,
            package=package,
            produced_signals=("strength_score", "strength_level"),
            consumed_signals=("season", "season_phase", "month_status"),
            chart_facts=chart_subset(context.chart, STRENGTH_CHART_KEYS),
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
            messages=("strength_package_bound",),
        )
