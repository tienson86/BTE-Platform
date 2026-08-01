"""Pipeline orchestration infrastructure tests (mock stages only)."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.exceptions.pipeline_error import InterpretationPipelineError
from engines.interpretation_engine.pipeline import (
    ExecutionHooks,
    ExecutionPolicy,
    ExecutionStatus,
    NoOpExecutionHooks,
    Pipeline,
    PipelineContext,
    PipelineExecutor,
    StageExecutor,
)
from engines.interpretation_engine.pipeline.execution_context import ExecutionContext
from engines.interpretation_engine.pipeline.execution_result import ExecutionResult, StageOutcome
from engines.interpretation_engine.pipeline.execution_state import ExecutionState
from tests.interpretation_engine.mocks import MockErrorStage, MockFailStage, MockSuccessStage


class CountingHooks(ExecutionHooks):
    """Test hooks that count lifecycle callbacks."""

    def __init__(self) -> None:
        self.before_pipeline_count = 0
        self.after_pipeline_count = 0
        self.before_stage_count = 0
        self.after_stage_count = 0
        self.error_count = 0

    def before_pipeline(self, context, state) -> None:
        self.before_pipeline_count += 1

    def after_pipeline(self, context, state, result) -> None:
        self.after_pipeline_count += 1

    def before_stage(self, stage, context, state) -> None:
        self.before_stage_count += 1

    def after_stage(self, stage, context, state, outcome) -> None:
        self.after_stage_count += 1

    def on_error(self, stage, context, state, error) -> None:
        self.error_count += 1


class TestPipelineOrchestration:
    """Mock-only pipeline orchestration coverage."""

    def test_deterministic_order_and_hooks(
        self,
        pipeline_context_stub: PipelineContext,
    ) -> None:
        """Stages run by (order, stage_id); hooks fire."""
        hooks = CountingHooks()
        pipeline = Pipeline(
            pipeline_id="interp_pipeline",
            stages=(
                MockSuccessStage(stage_id="b", order=2),
                MockSuccessStage(stage_id="a", order=1),
            ),
            hooks=hooks,
        )
        result = pipeline.run(pipeline_context_stub, execution_id="exec_1")
        assert result.success is True
        assert result.status == ExecutionStatus.SUCCEEDED
        assert result.stage_ids() == ("a", "b")
        assert result.outcome_for("a") is not None
        assert hooks.before_pipeline_count == 1
        assert hooks.after_stage_count == 2
        assert hooks.after_pipeline_count == 1

    def test_fail_fast_and_partial(
        self,
        pipeline_context_stub: PipelineContext,
    ) -> None:
        """Fail-fast stops; partial policy continues."""
        fail_fast = Pipeline(
            pipeline_id="interp_pipeline",
            stages=(
                MockFailStage(stage_id="fail", order=1),
                MockSuccessStage(stage_id="skip", order=2),
            ),
            policy=ExecutionPolicy(fail_fast=True),
        ).run(pipeline_context_stub)
        assert fail_fast.success is False
        assert fail_fast.stage_ids() == ("fail",)

        partial = Pipeline(
            pipeline_id="interp_pipeline",
            stages=(
                MockFailStage(stage_id="fail", order=1),
                MockSuccessStage(stage_id="ok", order=2),
            ),
            policy=ExecutionPolicy(fail_fast=False, allow_partial_success=True),
        ).run(pipeline_context_stub)
        assert partial.success is True
        assert partial.status == ExecutionStatus.PARTIAL
        assert partial.stage_ids() == ("fail", "ok")

    def test_stage_error_normalized(
        self,
        pipeline_context_stub: PipelineContext,
    ) -> None:
        """Runtime errors become failed outcomes."""
        result = Pipeline(
            pipeline_id="interp_pipeline",
            stages=(MockErrorStage(stage_id="boom", order=1),),
        ).run(pipeline_context_stub)
        assert result.success is False
        assert any("stage_execution_error" in msg for msg in result.errors)

    def test_pipeline_error_reraised_through_retries(
        self,
        pipeline_context_stub: PipelineContext,
    ) -> None:
        """InterpretationPipelineError from stage is caught at retry boundary."""
        hooks = CountingHooks()
        executor = PipelineExecutor(hooks=hooks)
        context = ExecutionContext.from_pipeline_context(
            execution_id="exec_pe",
            pipeline_context=pipeline_context_stub,
            policy=ExecutionPolicy(max_attempts=2),
        )
        result = executor.execute(
            stages=(MockErrorStage(stage_id="pe", order=1, raise_pipeline_error=True),),
            context=context,
        )
        assert result.success is False
        assert hooks.error_count >= 1

    def test_missing_required_stage_raises(
        self,
        pipeline_context_stub: PipelineContext,
    ) -> None:
        """Required stage policy validates presence."""
        executor = PipelineExecutor()
        context = ExecutionContext.from_pipeline_context(
            execution_id="exec_req",
            pipeline_context=pipeline_context_stub,
            policy=ExecutionPolicy(required_stage_ids=("needed",)),
        )
        with pytest.raises(InterpretationPipelineError, match="missing_required_stages"):
            executor.execute(
                stages=(MockSuccessStage(stage_id="other", order=1),),
                context=context,
            )

    def test_non_deterministic_preserves_input_order(
        self,
        pipeline_context_stub: PipelineContext,
    ) -> None:
        """Non-deterministic policy keeps provided stage order."""
        result = Pipeline(
            pipeline_id="interp_pipeline",
            stages=(
                MockSuccessStage(stage_id="z", order=1),
                MockSuccessStage(stage_id="a", order=1),
            ),
            policy=ExecutionPolicy(deterministic=False),
        ).run(pipeline_context_stub)
        assert result.stage_ids() == ("z", "a")

    def test_stage_id_normalization_and_validate_describe(
        self,
        pipeline_context_stub: PipelineContext,
    ) -> None:
        """Stage executor normalizes mismatched stage ids; pipeline validate/describe."""
        stage = MockSuccessStage(stage_id="norm", order=1, wrong_stage_id=True)
        outcome = StageExecutor().execute(stage, pipeline_context_stub)
        assert outcome.stage_id == "norm"
        assert any("stage_id_normalized" in msg for msg in outcome.messages)

        pipeline = Pipeline(pipeline_id="interp_pipeline", name="demo")
        assert pipeline.validate(pipeline_context_stub) is True
        assert pipeline.validate(PipelineContext(context_id="", pipeline_id="x")) is False
        bad = PipelineContext(context_id="c", pipeline_id="other")
        assert pipeline.validate(bad) is False
        assert pipeline.describe()["stage_count"] == "0"
        adapted = pipeline.run_as_pipeline_result(pipeline_context_stub)
        assert adapted.success is True

    def test_execution_context_helpers_and_noop_hooks(
        self,
        pipeline_context_stub: PipelineContext,
    ) -> None:
        """ExecutionContext helpers and no-op hooks are callable."""
        ctx = ExecutionContext.from_pipeline_context(
            execution_id="exec_ctx",
            pipeline_context=pipeline_context_stub,
        )
        assert ctx.to_pipeline_context().context_id == "pipe_ctx_1"
        updated = ctx.with_stage_output("s1", {"ok": True})
        assert "s1" in updated.stage_outputs
        assert pipeline_context_stub.get_attribute("source") == "test_stub"
        pipeline_context_stub.set_attribute("k", "v")
        assert pipeline_context_stub.get_stage_output("missing") is None

        hooks = NoOpExecutionHooks()
        state = ExecutionState(
            execution_id="e",
            pipeline_id="p",
            status=ExecutionStatus.RUNNING,
        )
        hooks.before_pipeline(ctx, state)
        hooks.before_stage(MockSuccessStage(), ctx, state)
        hooks.after_stage(
            MockSuccessStage(),
            ctx,
            state,
            StageOutcome(stage_id="x", success=True),
        )
        hooks.on_error(None, ctx, state, RuntimeError("x"))
        hooks.after_pipeline(
            ctx,
            state,
            ExecutionResult(
                execution_id="e",
                pipeline_id="p",
                success=True,
                status=ExecutionStatus.SUCCEEDED,
            ),
        )

    def test_empty_pipeline_succeeds(
        self,
        pipeline_context_stub: PipelineContext,
    ) -> None:
        """Empty stage list is a successful empty run."""
        result = Pipeline(pipeline_id="interp_pipeline").run(pipeline_context_stub)
        assert result.success is True
        assert result.status == ExecutionStatus.SUCCEEDED

    def test_pipeline_id_rewritten_on_context(
        self,
        pipeline_context_stub: PipelineContext,
    ) -> None:
        """Pipeline.run rewrites mismatched context pipeline_id."""
        pipeline_context_stub.pipeline_id = "other"
        result = Pipeline(
            pipeline_id="interp_pipeline",
            stages=(MockSuccessStage(stage_id="only", order=1),),
        ).run(pipeline_context_stub)
        assert result.pipeline_id == "interp_pipeline"
        assert pipeline_context_stub.pipeline_id == "interp_pipeline"
