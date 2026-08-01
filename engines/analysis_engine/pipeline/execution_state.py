"""Pipeline execution state for orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.analysis_engine.types.status import ExecutionStatus

_UNSET: Any = object()


@dataclass(frozen=True, slots=True)
class ExecutionState:
    """Immutable snapshot of pipeline orchestration state."""

    execution_id: str
    pipeline_id: str
    status: ExecutionStatus
    current_stage_id: str | None = None
    completed_stage_ids: tuple[str, ...] = ()
    failed_stage_id: str | None = None
    attempt: int = 1

    def transition(
        self,
        *,
        status: ExecutionStatus | None = None,
        current_stage_id: Any = _UNSET,
        append_completed: str | None = None,
        failed_stage_id: Any = _UNSET,
        attempt: int | None = None,
    ) -> ExecutionState:
        """Return a new state snapshot with updated orchestration fields."""
        completed = self.completed_stage_ids
        if append_completed is not None:
            completed = completed + (append_completed,)
        return ExecutionState(
            execution_id=self.execution_id,
            pipeline_id=self.pipeline_id,
            status=status if status is not None else self.status,
            current_stage_id=(
                self.current_stage_id
                if current_stage_id is _UNSET
                else current_stage_id
            ),
            completed_stage_ids=completed,
            failed_stage_id=(
                self.failed_stage_id
                if failed_stage_id is _UNSET
                else failed_stage_id
            ),
            attempt=attempt if attempt is not None else self.attempt,
        )
