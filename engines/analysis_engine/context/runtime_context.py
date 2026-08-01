"""Analysis Engine runtime context model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engines.analysis_engine.context.interfaces import ContextInterface


@dataclass(slots=True)
class RuntimeContext(ContextInterface):
    """Public contract for runtime analysis context."""

    id: str
    pipeline_id: str | None = None
    chart_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    stage_outputs: dict[str, Any] = field(default_factory=dict)

    def context_id(self) -> str:
        """Return the context identifier."""
        return self.id

    def get(self, key: str) -> Any:
        """Return a context value by key."""
        return self.attributes.get(key)

    def set(self, key: str, value: Any) -> None:
        """Assign a context value by key."""
        self.attributes[key] = value

    def get_stage_output(self, stage_id: str) -> Any:
        """Return output produced by a prior stage."""
        return self.stage_outputs.get(stage_id)
