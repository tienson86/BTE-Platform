"""Additional pipeline infrastructure edge-case tests."""

from __future__ import annotations

from engines.analysis_engine.pipeline.contracts import (
    ExecutionPolicyContract,
    RetryPolicyContract,
)
from engines.analysis_engine.pipeline.execution_context import ExecutionContext
from engines.analysis_engine.pipeline.execution_policy import ExecutionPolicy
from engines.analysis_engine.pipeline.execution_result import ExecutionResult
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext
from engines.analysis_engine.pipeline.pipeline_result import StageOutcome
from engines.analysis_engine.pipeline.stage_finalizer import StageFinalizer
from engines.analysis_engine.types.status import ExecutionStatus
from tests.analysis_engine.mocks import MockSuccessStage


class TestPipelineInfrastructureEdges:
    """Extra coverage for policy/context/result helpers."""

    def test_execution_policy_from_contract_and_context_helpers(self) -> None:
        """Policy/contracts and execution context helpers should work."""
        contract = ExecutionPolicyContract(
            policy_id="p1",
            fail_fast=False,
            allow_partial_success=True,
            required_stage_ids=("s1",),
            retry_policy=RetryPolicyContract(max_attempts=2),
        )
        policy = ExecutionPolicy.from_contract(contract)
        assert policy.max_attempts == 2
        assert policy.fail_fast is False

        pipeline_context = PipelineContext(
            context_id="c1",
            pipeline_id="pipe",
            attributes={"a": 1},
        )
        assert pipeline_context.get_attribute("a") == 1
        pipeline_context.set_attribute("b", 2)
        assert pipeline_context.get_attribute("b") == 2

        exec_ctx = ExecutionContext.from_pipeline_context(
            execution_id="e1",
            pipeline_context=pipeline_context,
            policy=policy,
        )
        updated = exec_ctx.with_stage_output("s1", {"ok": True})
        assert "s1" in updated.stage_outputs
        material = updated.to_pipeline_context()
        assert material.get_stage_output("s1") == {"ok": True}

        result = ExecutionResult(
            execution_id="e1",
            pipeline_id="pipe",
            success=True,
            status=ExecutionStatus.SUCCEEDED,
            outcomes=(
                StageOutcome(stage_id="s1", success=True, payload={"x": 1}),
            ),
        )
        assert result.stage_ids() == ("s1",)
        assert result.outcome_for("s1") is not None
        assert result.outcome_for("missing") is None

        stage = MockSuccessStage(stage_id="s1")
        finalizer = StageFinalizer()
        outcome = StageOutcome(stage_id="s1", success=True, payload={"n": 1})
        finalizer.finalize_stage(stage, material, outcome)
        assert material.stage_outputs["s1"] == {"n": 1}
        pipeline_result = finalizer.finalize_pipeline(material, (outcome,))
        assert pipeline_result.success is True
