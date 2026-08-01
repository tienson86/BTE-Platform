"""Interpretation pipeline stage executor for orchestration."""

from __future__ import annotations

from engines.interpretation_engine.exceptions.pipeline_error import InterpretationPipelineError
from engines.interpretation_engine.pipeline.execution_context import PipelineContext
from engines.interpretation_engine.pipeline.execution_result import StageOutcome
from engines.interpretation_engine.pipeline.stage_base import StageBase


class StageExecutor:
    """Orchestrates prepare → execute → finalize for a single interpretation stage.

    Does not evaluate rules or produce BaZi interpretation content.
    """

    def execute(self, stage: StageBase, context: PipelineContext) -> StageOutcome:
        """Execute a stage against the provided context."""
        self.execute_prepare(stage, context)
        outcome = self.execute_body(stage, context)
        stage.finalize(context, outcome)
        return outcome

    def execute_prepare(self, stage: StageBase, context: PipelineContext) -> None:
        """Run the stage prepare phase."""
        stage.prepare(context)

    def execute_body(self, stage: StageBase, context: PipelineContext) -> StageOutcome:
        """Run the stage execute phase and normalize the outcome."""
        try:
            outcome = stage.execute(context)
        except InterpretationPipelineError:
            raise
        except Exception as exc:  # noqa: BLE001 - orchestration boundary
            return StageOutcome(
                stage_id=stage.stage_id,
                success=False,
                payload={},
                messages=(f"stage_execution_error:{type(exc).__name__}:{exc}",),
            )
        if outcome.stage_id != stage.stage_id:
            return StageOutcome(
                stage_id=stage.stage_id,
                success=outcome.success,
                payload=dict(outcome.payload),
                messages=outcome.messages + (f"stage_id_normalized:{outcome.stage_id}",),
            )
        return outcome
