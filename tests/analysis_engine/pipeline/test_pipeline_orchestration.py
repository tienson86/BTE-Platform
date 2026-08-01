"""Pipeline orchestration integration tests."""

from __future__ import annotations

import pytest

from engines.analysis_engine.pipeline.execution_hooks import (
    ExecutionHooks,
    NoOpExecutionHooks,
)
from engines.analysis_engine.pipeline.execution_policy import ExecutionPolicy
from engines.analysis_engine.pipeline.executor import Executor
from engines.analysis_engine.pipeline.pipeline import Pipeline
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext
from engines.analysis_engine.pipeline.stage_executor import StageExecutor
from engines.analysis_engine.types.status import ExecutionStatus
from tests.analysis_engine.mocks import MockErrorStage, MockFailStage, MockSuccessStage


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


class TestPipelineOrchestrationIntegration:
    """Integration coverage for pipeline runtime orchestration."""

    def test_executor_runs_stages_in_deterministic_order(
        self,
        pipeline_context_stub: PipelineContext,
    ) -> None:
        """Stages should run by (order, stage_id) when deterministic."""
        late = MockSuccessStage(stage_id="b", order=2, payload={"n": 2})
        early = MockSuccessStage(stage_id="a", order=1, payload={"n": 1})
        hooks = CountingHooks()
        result = Executor(hooks=hooks).run(
            stages=(late, early),
            pipeline_context=pipeline_context_stub,
            execution_id="exec-order",
        )
        assert result.success is True
        assert result.status == ExecutionStatus.SUCCEEDED
        assert result.stage_ids() == ("a", "b")
        assert early.prepared and early.finalized
        assert hooks.before_pipeline_count == 1
        assert hooks.after_stage_count == 2

    def test_fail_fast_stops_after_first_failure(
        self,
        pipeline_context_stub: PipelineContext,
    ) -> None:
        """Fail-fast policy should skip later stages."""
        failing = MockFailStage(stage_id="fail", order=1)
        later = MockSuccessStage(stage_id="later", order=2)
        result = Executor(policy=ExecutionPolicy(fail_fast=True)).run(
            stages=(failing, later),
            pipeline_context=pipeline_context_stub,
            execution_id="exec-fail-fast",
        )
        assert result.success is False
        assert result.failed_stage_id == "fail"
        assert result.stage_ids() == ("fail",)

    def test_partial_success_policy(
        self,
        pipeline_context_stub: PipelineContext,
    ) -> None:
        """Non-fail-fast partial policy should continue after failure."""
        policy = ExecutionPolicy(fail_fast=False, allow_partial_success=True)
        result = Executor(policy=policy).run(
            stages=(
                MockFailStage(stage_id="fail", order=1),
                MockSuccessStage(stage_id="ok", order=2),
            ),
            pipeline_context=pipeline_context_stub,
            policy=policy,
            execution_id="exec-partial",
        )
        assert result.success is True
        assert result.status == ExecutionStatus.PARTIAL
        assert result.stage_ids() == ("fail", "ok")

    def test_stage_executor_normalizes_raised_errors(
        self,
        pipeline_context_stub: PipelineContext,
    ) -> None:
        """Stage executor should convert raised errors into failed outcomes."""
        outcome = StageExecutor().execute(
            MockErrorStage(),
            pipeline_context_stub,
        )
        assert outcome.success is False
        assert any("mock_stage_boom" in message for message in outcome.messages)

    def test_pipeline_facade_run_as_pipeline_result(
        self,
        pipeline_context_stub: PipelineContext,
    ) -> None:
        """Pipeline facade should adapt execution into PipelineResult."""
        pipeline = Pipeline(
            "test_pipeline",
            stages=(MockSuccessStage(stage_id="s1", order=1),),
        )
        result = pipeline.run(pipeline_context_stub)
        assert result.success is True
        assert result.outcome_for("s1") is not None
        assert pipeline.validate(pipeline_context_stub) is True
        assert pipeline.describe()["pipeline_id"] == "test_pipeline"

    def test_required_stage_missing_raises(self) -> None:
        """Missing required stages should raise PipelineError."""
        from engines.analysis_engine.exceptions.pipeline_error import PipelineError

        policy = ExecutionPolicy(required_stage_ids=("must_exist",))
        with pytest.raises(PipelineError):
            Executor(policy=policy).run(
                stages=(MockSuccessStage(stage_id="other"),),
                pipeline_context=PipelineContext(
                    context_id="c",
                    pipeline_id="p",
                ),
                policy=policy,
            )

    def test_noop_hooks_are_safe(
        self,
        pipeline_context_stub: PipelineContext,
    ) -> None:
        """Default no-op hooks should not alter orchestration."""
        result = Executor(hooks=NoOpExecutionHooks()).run(
            stages=(MockSuccessStage(),),
            pipeline_context=pipeline_context_stub,
        )
        assert result.success is True
