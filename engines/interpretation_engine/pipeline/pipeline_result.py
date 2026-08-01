"""Interpretation pipeline result contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class InterpretationPipelineResult:
    """Immutable pipeline execution result shell."""

    id: str
    pipeline_id: str
    success: bool
    stage_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)
    errors: tuple[str, ...] = ()

    def validate(self) -> bool:
        """Validate pipeline result structure."""
        return bool(self.id and self.pipeline_id)
