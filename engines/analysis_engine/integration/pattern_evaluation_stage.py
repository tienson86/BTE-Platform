"""Pattern Evaluation knowledge-package integration stage."""

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

EVALUATION_CHART_KEYS: tuple[str, ...] = (
    "pattern_quality",
    "pattern_confidence",
    "pattern_integrity",
    "pattern_stability",
    "pattern_score",
)


class PatternEvaluationStage:
    """Bind Pattern Evaluation. Does not re-identify principal pattern."""

    stage_id: str = "pattern_evaluation"
    name: str = "Pattern Evaluation"
    version: str = "1.0.0"
    order: int = 70
    package_id: str = "bz_05_pattern_evaluation"

    def dependencies(self) -> tuple[str, ...]:
        """Evaluation consumes Pattern Core plus score-band stages."""
        return ("pattern", "seasonal", "strength", "temperature")

    def execute(
        self,
        context: AnalysisExecutionContext,
        package: LoadedPackage,
    ) -> Mapping[str, Any]:
        """Publish Pattern Evaluation binding after Pattern Core."""
        require_upstream(context, self.stage_id, self.dependencies())
        payload = bind_package_payload(
            stage_id=self.stage_id,
            package=package,
            produced_signals=(
                "pattern_quality",
                "pattern_confidence",
                "pattern_integrity",
                "pattern_stability",
                "pattern_score",
                "evaluation_diagnostics",
            ),
            consumed_signals=(
                "principal_pattern",
                "pattern_confirmed",
                "pattern_conflict",
                "pattern_suppressed",
                "core_pattern_score",
                "season_score",
                "strength_score",
                "temperature_score",
            ),
            chart_facts=chart_subset(context.chart, EVALUATION_CHART_KEYS),
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
            messages=("pattern_evaluation_package_bound",),
        )
