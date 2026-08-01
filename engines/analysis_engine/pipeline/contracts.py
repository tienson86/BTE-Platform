"""Pipeline contracts.

Contract declarations only. No pipeline execution logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class StageContract:
    """Contract describing a pipeline stage identity and surface."""

    stage_id: str
    name: str
    version: str = "0.0.0"
    order: int = 0
    required_fields: tuple[str, ...] = (
        "stage_id",
        "name",
        "version",
        "order",
    )
    optional_fields: tuple[str, ...] = ("dependencies",)


@dataclass(frozen=True, slots=True)
class PipelineContextContract:
    """Contract describing pipeline-level context requirements."""

    context_type: str = "PipelineContext"
    required_fields: tuple[str, ...] = (
        "context_id",
        "pipeline_id",
    )
    optional_fields: tuple[str, ...] = (
        "chart_id",
        "attributes",
        "stage_outputs",
    )


@dataclass(frozen=True, slots=True)
class StageContextContract:
    """Contract describing stage-local context requirements."""

    context_type: str = "StageContext"
    required_fields: tuple[str, ...] = (
        "context_id",
        "pipeline_id",
        "stage_id",
    )
    optional_fields: tuple[str, ...] = (
        "chart_id",
        "attributes",
        "upstream_outputs",
    )


@dataclass(frozen=True, slots=True)
class StageResultContract:
    """Contract describing stage result shape."""

    result_type: str = "StageResult"
    required_fields: tuple[str, ...] = (
        "id",
        "version",
        "metadata",
        "trace",
        "timestamps",
        "stage_id",
        "success",
    )
    optional_fields: tuple[str, ...] = (
        "scores",
        "decisions",
        "payload",
    )


@dataclass(frozen=True, slots=True)
class ExecutionResultContract:
    """Contract describing successful pipeline execution result shape."""

    result_type: str = "ExecutionResult"
    required_fields: tuple[str, ...] = (
        "execution_id",
        "pipeline_id",
        "success",
        "stage_result_ids",
    )
    optional_fields: tuple[str, ...] = (
        "messages",
        "metadata",
        "trace",
        "timestamps",
    )


@dataclass(frozen=True, slots=True)
class FailureResultContract:
    """Contract describing pipeline failure result shape."""

    result_type: str = "FailureResult"
    required_fields: tuple[str, ...] = (
        "execution_id",
        "pipeline_id",
        "success",
        "error_code",
        "error_message",
    )
    optional_fields: tuple[str, ...] = (
        "failed_stage_id",
        "retriable",
        "trace",
        "timestamps",
    )
    success: bool = False


@dataclass(frozen=True, slots=True)
class RetryPolicyContract:
    """Contract describing retry behavior for pipeline execution."""

    policy_id: str = "default_retry_policy"
    max_attempts: int = 1
    backoff_strategy: str = "none"
    retriable_error_codes: tuple[str, ...] = ()
    non_retriable_error_codes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ExecutionPolicyContract:
    """Contract describing pipeline execution policy constraints."""

    policy_id: str = "default_execution_policy"
    deterministic: bool = True
    fail_fast: bool = True
    allow_partial_success: bool = False
    required_stage_ids: tuple[str, ...] = ()
    optional_stage_ids: tuple[str, ...] = ()
    retry_policy: RetryPolicyContract = field(default_factory=RetryPolicyContract)


@dataclass(frozen=True, slots=True)
class PipelineContracts:
    """Aggregate contract surface for the Analysis Engine pipeline."""

    stage: StageContract = field(
        default_factory=lambda: StageContract(stage_id="", name="")
    )
    pipeline_context: PipelineContextContract = field(
        default_factory=PipelineContextContract
    )
    stage_context: StageContextContract = field(default_factory=StageContextContract)
    stage_result: StageResultContract = field(default_factory=StageResultContract)
    execution_result: ExecutionResultContract = field(
        default_factory=ExecutionResultContract
    )
    failure_result: FailureResultContract = field(default_factory=FailureResultContract)
    retry_policy: RetryPolicyContract = field(default_factory=RetryPolicyContract)
    execution_policy: ExecutionPolicyContract = field(
        default_factory=ExecutionPolicyContract
    )
