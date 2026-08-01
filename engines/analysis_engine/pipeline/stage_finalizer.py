"""Stage finalizer for orchestration."""

from __future__ import annotations

from engines.analysis_engine.pipeline.pipeline_context import PipelineContext
from engines.analysis_engine.pipeline.pipeline_result import (
    PipelineResult,
    StageOutcome,
)
from engines.analysis_engine.pipeline.stage_base import StageBase


class StageFinalizer:
    """Finalizes stage and pipeline outcomes for orchestration."""

    def finalize_stage(
        self,
        stage: StageBase,
        context: PipelineContext,
        outcome: StageOutcome,
    ) -> None:
        """Record stage payload onto the pipeline context when successful."""
        if outcome.success:
            context.stage_outputs[stage.stage_id] = dict(outcome.payload)

    def finalize_pipeline(
        self,
        context: PipelineContext,
        outcomes: tuple[StageOutcome, ...],
    ) -> PipelineResult:
        """Finalize the full pipeline into a public result contract."""
        errors = tuple(
            message
            for outcome in outcomes
            if not outcome.success
            for message in outcome.messages
        )
        success = all(outcome.success for outcome in outcomes) if outcomes else True
        return PipelineResult(
            pipeline_id=context.pipeline_id,
            success=success,
            outcomes=outcomes,
            errors=errors,
        )
