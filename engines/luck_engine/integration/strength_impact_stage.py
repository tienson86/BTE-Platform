"""Strength analytical impact. Structural overlap with day master identity."""

from __future__ import annotations

from engines.luck_engine.analysis.analysis_context import LuckAnalysisContext
from engines.luck_engine.analysis.impact_models import StageImpact
from engines.luck_engine.analysis_constants import STAGE_SEASONAL, STAGE_STRENGTH
from engines.luck_engine.integration.base_stage import (
    build_stage_impact,
    iter_timeline_periods,
    natal_tokens,
    require_dependencies,
    snapshot_tokens,
)


class StrengthImpactStage:
    """Publish strength_impact from timeline × day-pillar / strength snapshot."""

    stage_id = STAGE_STRENGTH
    dependencies: tuple[str, ...] = (STAGE_SEASONAL,)

    def execute(self, context: LuckAnalysisContext) -> StageImpact:
        """Measure day-pillar overlap. Does not recompute strength_score."""
        require_dependencies(context, self.dependencies, self.stage_id)
        natal, natal_fields = natal_tokens(
            context.timeline_snapshot,
            ("day_pillar",),
        )
        strength = context.analysis_snapshot.get("strength")
        extra, present = snapshot_tokens(
            strength if isinstance(strength, dict) else None,
            ("day_master", "strength_level"),
        )
        reference = natal | extra
        return build_stage_impact(
            stage_id=self.stage_id,
            periods=iter_timeline_periods(context.timeline_snapshot),
            reference=reference,
            consumed_fields=natal_fields + present,
            reference_present=bool(reference),
        )
