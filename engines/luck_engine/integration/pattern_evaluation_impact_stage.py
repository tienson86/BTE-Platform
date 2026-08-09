"""Pattern Evaluation analytical impact. Completeness-aware structural overlap."""

from __future__ import annotations

from engines.luck_engine.analysis.analysis_context import LuckAnalysisContext
from engines.luck_engine.analysis.impact_models import StageImpact
from engines.luck_engine.analysis_constants import STAGE_PATTERN, STAGE_PATTERN_EVALUATION
from engines.luck_engine.integration.base_stage import (
    build_stage_impact,
    iter_timeline_periods,
    natal_tokens,
    require_dependencies,
    snapshot_tokens,
)


class PatternEvaluationImpactStage:
    """Publish pattern_evaluation_impact from evaluation identity tokens."""

    stage_id = STAGE_PATTERN_EVALUATION
    dependencies: tuple[str, ...] = (STAGE_PATTERN,)

    def execute(self, context: LuckAnalysisContext) -> StageImpact:
        """Consume evaluation identity only. Does not judge pattern quality."""
        require_dependencies(context, self.dependencies, self.stage_id)
        natal, natal_fields = natal_tokens(
            context.timeline_snapshot,
            ("day_pillar",),
        )
        evaluation = context.analysis_snapshot.get("pattern_evaluation")
        extra, present = snapshot_tokens(
            evaluation if isinstance(evaluation, dict) else None,
            ("pattern_quality", "pattern_confidence"),
        )
        reference = natal | extra
        return build_stage_impact(
            stage_id=self.stage_id,
            periods=iter_timeline_periods(context.timeline_snapshot),
            reference=reference,
            consumed_fields=natal_fields + present,
            reference_present=bool(reference),
        )
