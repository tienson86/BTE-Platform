"""Pipeline context model skeleton."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PipelineContext:
    """Public context contract passed through pipeline execution."""

    context_id: str
    pipeline_id: str
    chart_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    stage_outputs: dict[str, Any] = field(default_factory=dict)

    def get_attribute(self, key: str) -> Any:
        """Return a context attribute by key."""
        raise NotImplementedError

    def set_attribute(self, key: str, value: Any) -> None:
        """Assign a context attribute by key."""
        raise NotImplementedError

    def get_stage_output(self, stage_id: str) -> Any:
        """Return output produced by a prior stage."""
        raise NotImplementedError
