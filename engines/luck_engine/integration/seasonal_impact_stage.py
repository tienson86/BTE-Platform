"""Seasonal analytical impact. Structural overlap with natal month / seasonal snapshot."""

from __future__ import annotations

from engines.luck_engine.analysis.analysis_context import LuckAnalysisContext
from engines.luck_engine.analysis.impact_models import StageImpact
from engines.luck_engine.analysis_constants import STAGE_SEASONAL
from engines.luck_engine.integration.base_stage import (
    build_stage_impact,
    iter_timeline_periods,
    natal_tokens,
    snapshot_tokens,
)


class SeasonalImpactStage:
    """Publish seasonal_impact from timeline × seasonal published identity."""

    stage_id = STAGE_SEASONAL
    dependencies: tuple[str, ...] = ()

    def execute(self, context: LuckAnalysisContext) -> StageImpact:
        """Measure month-pillar / seasonal identity overlap. No seasonal scoring."""
        natal, natal_fields = natal_tokens(
            context.timeline_snapshot,
            ("month_pillar",),
        )
        seasonal = context.analysis_snapshot.get("seasonal")
        extra, present = snapshot_tokens(
            seasonal if isinstance(seasonal, dict) else None,
            ("season", "season_phase", "month_branch"),
        )
        reference = natal | extra
        consumed = natal_fields + present
        return build_stage_impact(
            stage_id=self.stage_id,
            periods=iter_timeline_periods(context.timeline_snapshot),
            reference=reference,
            consumed_fields=consumed,
            reference_present=bool(reference),
        )
