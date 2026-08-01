"""Pipeline execution policy for orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field

from engines.analysis_engine.pipeline.contracts import (
    ExecutionPolicyContract,
    RetryPolicyContract,
)


@dataclass(frozen=True, slots=True)
class ExecutionPolicy:
    """Immutable runtime execution policy for pipeline orchestration."""

    policy_id: str = "default_execution_policy"
    deterministic: bool = True
    fail_fast: bool = True
    allow_partial_success: bool = False
    required_stage_ids: tuple[str, ...] = ()
    optional_stage_ids: tuple[str, ...] = ()
    max_attempts: int = 1
    retry_policy_id: str = "default_retry_policy"

    @classmethod
    def from_contract(cls, contract: ExecutionPolicyContract) -> ExecutionPolicy:
        """Build a runtime policy from an execution policy contract."""
        retry: RetryPolicyContract = contract.retry_policy
        return cls(
            policy_id=contract.policy_id,
            deterministic=contract.deterministic,
            fail_fast=contract.fail_fast,
            allow_partial_success=contract.allow_partial_success,
            required_stage_ids=contract.required_stage_ids,
            optional_stage_ids=contract.optional_stage_ids,
            max_attempts=max(1, retry.max_attempts),
            retry_policy_id=retry.policy_id,
        )

    @classmethod
    def default(cls) -> ExecutionPolicy:
        """Return the default deterministic fail-fast policy."""
        return cls()
