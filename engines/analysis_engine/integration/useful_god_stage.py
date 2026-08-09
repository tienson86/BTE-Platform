"""Useful God Decision Foundation integration stage."""

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

USEFUL_GOD_CHART_KEYS: tuple[str, ...] = (
    "season_score",
    "strength_score",
    "temperature_score",
    "pattern_score",
    "pattern_quality",
    "pattern_confidence",
    "pattern_integrity",
    "pattern_stability",
    "useful_god",
)


class UsefulGodStage:
    """Bind Useful God Decision. Consumes published outputs only."""

    stage_id: str = "useful_god"
    name: str = "Useful God"
    version: str = "1.0.0"
    order: int = 80
    package_id: str = "bz_06_useful_god_foundation"

    def dependencies(self) -> tuple[str, ...]:
        """Useful God consumes score bands and Pattern Evaluation."""
        return (
            "seasonal",
            "strength",
            "temperature",
            "pattern",
            "pattern_evaluation",
        )

    def execute(
        self,
        context: AnalysisExecutionContext,
        package: LoadedPackage,
    ) -> Mapping[str, Any]:
        """Publish Useful God decision binding. Does not recompute upstream."""
        require_upstream(context, self.stage_id, self.dependencies())
        payload = bind_package_payload(
            stage_id=self.stage_id,
            package=package,
            produced_signals=(
                "useful_god",
                "favorable_gods",
                "unfavorable_gods",
                "decision_confidence",
                "decision_score",
                "decision_reasoning",
                "decision_diagnostics",
            ),
            consumed_signals=(
                "season_score",
                "strength_score",
                "temperature_score",
                "pattern_score",
                "pattern_quality",
                "pattern_confidence",
                "pattern_integrity",
                "pattern_stability",
            ),
            chart_facts=chart_subset(context.chart, USEFUL_GOD_CHART_KEYS),
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
            messages=("useful_god_package_bound",),
        )
