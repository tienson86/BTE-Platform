"""Architecture tests for interpretation pipeline runtime."""

from __future__ import annotations

from engines.interpretation_engine.pipeline import (
    ExecutionPolicy,
    ExecutionStatus,
    Pipeline,
    PipelineContext,
    StageBase,
    StageOutcome,
)


class _PassStage(StageBase):
    """Minimal passing stage for orchestration smoke tests."""

    def prepare(self, context: PipelineContext) -> None:
        """No-op prepare."""
        return None

    def execute(self, context: PipelineContext) -> StageOutcome:
        """Return a successful empty outcome."""
        return StageOutcome(stage_id=self.stage_id, success=True, payload={"ok": True})

    def finalize(self, context: PipelineContext, outcome: StageOutcome) -> None:
        """No-op finalize."""
        return None


class _FailStage(StageBase):
    """Minimal failing stage for orchestration smoke tests."""

    def prepare(self, context: PipelineContext) -> None:
        """No-op prepare."""
        return None

    def execute(self, context: PipelineContext) -> StageOutcome:
        """Return a failed outcome."""
        return StageOutcome(
            stage_id=self.stage_id,
            success=False,
            messages=("stage_failed",),
        )

    def finalize(self, context: PipelineContext, outcome: StageOutcome) -> None:
        """No-op finalize."""
        return None


def test_pipeline_runs_ordered_stages() -> None:
    """Pipeline executes stages in deterministic order without business logic."""
    pipeline = Pipeline(
        pipeline_id="interp_pipe_1",
        stages=(
            _PassStage(stage_id="b", name="B", order=2),
            _PassStage(stage_id="a", name="A", order=1),
        ),
        policy=ExecutionPolicy.default(),
    )
    context = PipelineContext(context_id="ctx_1", pipeline_id="interp_pipe_1")
    result = pipeline.run(context)

    assert result.success is True
    assert result.status == ExecutionStatus.SUCCEEDED
    assert result.stage_ids() == ("a", "b")
    assert result.completed_stage_ids == ("a", "b")


def test_pipeline_fail_fast() -> None:
    """Fail-fast policy stops after the first failed stage."""
    pipeline = Pipeline(
        pipeline_id="interp_pipe_2",
        stages=(
            _FailStage(stage_id="fail", name="Fail", order=1),
            _PassStage(stage_id="skip", name="Skip", order=2),
        ),
        policy=ExecutionPolicy(fail_fast=True),
    )
    context = PipelineContext(context_id="ctx_2", pipeline_id="interp_pipe_2")
    result = pipeline.run(context)

    assert result.success is False
    assert result.status == ExecutionStatus.FAILED
    assert result.failed_stage_id == "fail"
    assert result.stage_ids() == ("fail",)


def test_run_as_pipeline_result() -> None:
    """Adapter produces InterpretationPipelineResult from execution result."""
    pipeline = Pipeline(
        pipeline_id="interp_pipe_3",
        stages=(_PassStage(stage_id="only", name="Only", order=1),),
    )
    context = PipelineContext(context_id="ctx_3", pipeline_id="interp_pipe_3")
    adapted = pipeline.run_as_pipeline_result(context)

    assert adapted.pipeline_id == "interp_pipe_3"
    assert adapted.success is True
    assert adapted.stage_ids == ("only",)
    assert adapted.validate() is True
