"""Pipeline result model skeleton."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class StageOutcome:
    """Public outcome contract for a single stage execution."""

    stage_id: str
    success: bool
    payload: dict[str, Any] = field(default_factory=dict)
    messages: tuple[str, ...] = ()


@dataclass(slots=True)
class PipelineResult:
    """Public result contract for a completed pipeline run."""

    pipeline_id: str
    success: bool
    outcomes: tuple[StageOutcome, ...] = ()
    errors: tuple[str, ...] = ()

    def stage_ids(self) -> tuple[str, ...]:
        """Return ordered stage identifiers present in the result."""
        raise NotImplementedError

    def outcome_for(self, stage_id: str) -> StageOutcome | None:
        """Return the outcome for a specific stage identifier."""
        raise NotImplementedError
