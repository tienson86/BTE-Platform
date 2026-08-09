"""Pattern Core knowledge-package integration stage."""

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

PATTERN_CHART_KEYS: tuple[str, ...] = (
    "day_master",
    "day_master_element",
    "month_branch",
    "principal_pattern",
    "pattern_score",
)


class PatternStage:
    """Bind Pattern Core. Does not recompute pattern identification."""

    stage_id: str = "pattern"
    name: str = "Pattern"
    version: str = "1.0.0"
    order: int = 60
    package_id: str = "bz_04_pattern_core"

    def dependencies(self) -> tuple[str, ...]:
        """Pattern consumes Four Pillars plus Seasonal/Strength/Temperature."""
        return ("four_pillars", "seasonal", "strength", "temperature")

    def execute(
        self,
        context: AnalysisExecutionContext,
        package: LoadedPackage,
    ) -> Mapping[str, Any]:
        """Publish Pattern Core binding after Temperature."""
        require_upstream(context, self.stage_id, self.dependencies())
        payload = bind_package_payload(
            stage_id=self.stage_id,
            package=package,
            produced_signals=(
                "principal_pattern",
                "pattern_confirmed",
                "pattern_conflict",
                "pattern_suppressed",
                "pattern_stability",
                "core_pattern_score",
            ),
            consumed_signals=(
                "season",
                "season_phase",
                "season_score",
                "strength_score",
                "temperature_score",
            ),
            chart_facts=chart_subset(context.chart, PATTERN_CHART_KEYS),
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
            messages=("pattern_package_bound",),
        )
