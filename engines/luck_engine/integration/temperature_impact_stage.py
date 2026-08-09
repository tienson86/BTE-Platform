"""Temperature analytical impact. Structural overlap with climate identity tokens."""

from __future__ import annotations

from engines.luck_engine.analysis.analysis_context import LuckAnalysisContext
from engines.luck_engine.analysis.impact_models import StageImpact
from engines.luck_engine.analysis_constants import (
    STAGE_SEASONAL,
    STAGE_STRENGTH,
    STAGE_TEMPERATURE,
)
from engines.luck_engine.integration.base_stage import (
    build_stage_impact,
    iter_timeline_periods,
    natal_tokens,
    require_dependencies,
    snapshot_tokens,
)


class TemperatureImpactStage:
    """Publish temperature_impact from month/day identity × temperature snapshot."""

    stage_id = STAGE_TEMPERATURE
    dependencies: tuple[str, ...] = (STAGE_SEASONAL, STAGE_STRENGTH)

    def execute(self, context: LuckAnalysisContext) -> StageImpact:
        """Measure climate-token overlap. Does not recompute temperature_score."""
        require_dependencies(context, self.dependencies, self.stage_id)
        natal, natal_fields = natal_tokens(
            context.timeline_snapshot,
            ("month_pillar", "day_pillar"),
        )
        temperature = context.analysis_snapshot.get("temperature")
        extra, present = snapshot_tokens(
            temperature if isinstance(temperature, dict) else None,
            ("temperature_level", "dryness_level", "humidity_level", "day_master_element"),
        )
        reference = natal | extra
        return build_stage_impact(
            stage_id=self.stage_id,
            periods=iter_timeline_periods(context.timeline_snapshot),
            reference=reference,
            consumed_fields=natal_fields + present,
            reference_present=bool(reference),
        )
