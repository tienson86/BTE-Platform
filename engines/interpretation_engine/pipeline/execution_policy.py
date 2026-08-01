"""Interpretation pipeline execution policy for orchestration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionPolicy:
    """Immutable runtime execution policy for interpretation pipeline orchestration."""

    policy_id: str = "default_interpretation_execution_policy"
    deterministic: bool = True
    fail_fast: bool = True
    allow_partial_success: bool = False
    required_stage_ids: tuple[str, ...] = ()
    optional_stage_ids: tuple[str, ...] = ()
    max_attempts: int = 1
    retry_policy_id: str = "default_interpretation_retry_policy"

    @classmethod
    def default(cls) -> ExecutionPolicy:
        """Return the default deterministic fail-fast policy."""
        return cls()
