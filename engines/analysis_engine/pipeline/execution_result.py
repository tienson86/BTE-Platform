"""Pipeline execution result for orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.pipeline.pipeline_result import StageOutcome
from engines.analysis_engine.types.status import ExecutionStatus


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """Immutable result of a pipeline orchestration run."""

    execution_id: str
    pipeline_id: str
    success: bool
    status: ExecutionStatus
    outcomes: tuple[StageOutcome, ...] = ()
    errors: tuple[str, ...] = ()
    completed_stage_ids: tuple[str, ...] = ()
    failed_stage_id: str | None = None
    messages: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def stage_ids(self) -> tuple[str, ...]:
        """Return ordered stage identifiers present in outcomes."""
        return tuple(outcome.stage_id for outcome in self.outcomes)

    def outcome_for(self, stage_id: str) -> StageOutcome | None:
        """Return the outcome for a specific stage identifier."""
        for outcome in self.outcomes:
            if outcome.stage_id == stage_id:
                return outcome
        return None
