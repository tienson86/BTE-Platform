"""Four Pillars passthrough stage. No knowledge package in AX-1."""

from __future__ import annotations

from typing import Any, Mapping

from engines.analysis_engine.integration.base_stage import chart_subset, require_upstream
from engines.analysis_engine.pipeline.execution_context import AnalysisExecutionContext
from engines.analysis_engine.pipeline.pipeline_result import StageOutcome

PILLAR_CHART_KEYS: tuple[str, ...] = (
    "year_pillar",
    "month_pillar",
    "day_pillar",
    "hour_pillar",
    "day_master",
    "day_master_element",
    "month_branch",
    "hidden_stems",
    "ten_gods",
)


class FourPillarsStage:
    """Publish Four Pillars chart facts for downstream knowledge stages."""

    stage_id: str = "four_pillars"
    name: str = "Four Pillars"
    version: str = "1.0.0"
    order: int = 20

    def dependencies(self) -> tuple[str, ...]:
        """Four Pillars consume Calendar outputs."""
        return ("calendar",)

    def execute(self, context: AnalysisExecutionContext) -> Mapping[str, Any]:
        """Pass pillar facts into the shared context."""
        require_upstream(context, self.stage_id, self.dependencies())
        payload = {
            "stage_id": self.stage_id,
            "status": "passthrough",
            "package_id": None,
            "produced_signals": (
                "day_master",
                "day_master_element",
                "month_branch",
                "pillars",
            ),
            "consumed_signals": ("normalized_datetime", "solar_term"),
            "upstream_stages": self.dependencies(),
            "chart_facts": chart_subset(context.chart, PILLAR_CHART_KEYS),
        }
        context.publish(self.stage_id, payload)
        return payload

    def as_outcome(self, payload: Mapping[str, Any]) -> StageOutcome:
        """Adapt the payload to the orchestration StageOutcome contract."""
        return StageOutcome(
            stage_id=self.stage_id,
            success=True,
            payload=dict(payload),
            messages=("four_pillars_passthrough",),
        )
