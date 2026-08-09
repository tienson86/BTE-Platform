"""Calendar passthrough stage. No knowledge package in AX-1."""

from __future__ import annotations

from typing import Any, Mapping

from engines.analysis_engine.integration.base_stage import chart_subset
from engines.analysis_engine.pipeline.execution_context import AnalysisExecutionContext
from engines.analysis_engine.pipeline.pipeline_result import StageOutcome

CALENDAR_CHART_KEYS: tuple[str, ...] = (
    "datetime",
    "timezone",
    "solar_term",
    "lunar_month_index",
)


class CalendarStage:
    """Publish calendar facts from the chart snapshot."""

    stage_id: str = "calendar"
    name: str = "Calendar"
    version: str = "1.0.0"
    order: int = 10

    def dependencies(self) -> tuple[str, ...]:
        """Calendar is the pipeline root."""
        return ()

    def execute(self, context: AnalysisExecutionContext) -> Mapping[str, Any]:
        """Pass calendar chart facts into the shared context."""
        payload = {
            "stage_id": self.stage_id,
            "status": "passthrough",
            "package_id": None,
            "produced_signals": ("normalized_datetime", "solar_term", "lunar_month_index"),
            "consumed_signals": (),
            "chart_facts": chart_subset(context.chart, CALENDAR_CHART_KEYS),
        }
        context.publish(self.stage_id, payload)
        return payload

    def as_outcome(self, payload: Mapping[str, Any]) -> StageOutcome:
        """Adapt the payload to the orchestration StageOutcome contract."""
        return StageOutcome(
            stage_id=self.stage_id,
            success=True,
            payload=dict(payload),
            messages=("calendar_passthrough",),
        )
