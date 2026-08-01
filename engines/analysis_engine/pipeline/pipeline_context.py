"""Pipeline context model for orchestration."""

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
        return self.attributes.get(key)

    def set_attribute(self, key: str, value: Any) -> None:
        """Assign a context attribute by key."""
        self.attributes[key] = value

    def get_stage_output(self, stage_id: str) -> Any:
        """Return output produced by a prior stage."""
        return self.stage_outputs.get(stage_id)
