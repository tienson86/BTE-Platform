"""Pattern analytical impact. Structural overlap with published pattern identity."""

from __future__ import annotations

from engines.luck_engine.analysis.analysis_context import LuckAnalysisContext
from engines.luck_engine.analysis.impact_models import StageImpact
from engines.luck_engine.analysis_constants import STAGE_PATTERN, STAGE_TEMPERATURE
from engines.luck_engine.integration.base_stage import (
    build_stage_impact,
    iter_timeline_periods,
    natal_tokens,
    require_dependencies,
    snapshot_tokens,
)


class PatternImpactStage:
    """Publish pattern_impact from timeline × principal pattern identity."""

    stage_id = STAGE_PATTERN
    dependencies: tuple[str, ...] = (STAGE_TEMPERATURE,)

    def execute(self, context: LuckAnalysisContext) -> StageImpact:
        """Measure pattern-token overlap. Does not confirm or break patterns."""
        require_dependencies(context, self.dependencies, self.stage_id)
        natal, natal_fields = natal_tokens(
            context.timeline_snapshot,
            ("day_pillar",),
        )
        pattern = context.analysis_snapshot.get("pattern")
        extra, present = snapshot_tokens(
            pattern if isinstance(pattern, dict) else None,
            ("principal_pattern",),
        )
        reference = natal | extra
        return build_stage_impact(
            stage_id=self.stage_id,
            periods=iter_timeline_periods(context.timeline_snapshot),
            reference=reference,
            consumed_fields=natal_fields + present,
            reference_present=bool(reference),
        )
