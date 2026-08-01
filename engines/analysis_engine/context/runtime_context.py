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
        raise NotImplementedError

    def get(self, key: str) -> Any:
        """Return a context value by key."""
        raise NotImplementedError

    def set(self, key: str, value: Any) -> None:
        """Assign a context value by key."""
        raise NotImplementedError

    def get_stage_output(self, stage_id: str) -> Any:
        """Return output produced by a prior stage."""
        raise NotImplementedError
