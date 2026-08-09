"""Useful God analytical impact. Identity co-occurrence only. No override."""

from __future__ import annotations

from engines.luck_engine.analysis.analysis_context import LuckAnalysisContext
from engines.luck_engine.analysis.impact_models import StageImpact
from engines.luck_engine.analysis_constants import (
    STAGE_PATTERN_EVALUATION,
    STAGE_USEFUL_GOD,
)
from engines.luck_engine.integration.base_stage import (
    build_stage_impact,
    iter_timeline_periods,
    require_dependencies,
    snapshot_tokens,
)


class UsefulGodImpactStage:
    """Publish useful_god_impact from published Useful God identity strings."""

    stage_id = STAGE_USEFUL_GOD
    dependencies: tuple[str, ...] = (STAGE_PATTERN_EVALUATION,)

    def execute(self, context: LuckAnalysisContext) -> StageImpact:
        """Measure co-occurrence with published gods. Does not change Useful God."""
        require_dependencies(context, self.dependencies, self.stage_id)
        analysis_ug = context.analysis_snapshot.get("useful_god")
        analysis_tokens, analysis_fields = snapshot_tokens(
            analysis_ug if isinstance(analysis_ug, dict) else None,
            ("useful_god", "favorable_gods", "unfavorable_gods"),
        )
        decision_tokens, decision_fields = snapshot_tokens(
            context.decision_snapshot,
            ("final_useful_god", "final_favorable_gods", "final_unfavorable_gods"),
        )
        reference = analysis_tokens | decision_tokens
        consumed = analysis_fields + tuple(f"decision.{name}" for name in decision_fields)
        return build_stage_impact(
            stage_id=self.stage_id,
            periods=iter_timeline_periods(context.timeline_snapshot),
            reference=reference,
            consumed_fields=consumed,
            reference_present=bool(reference),
        )
