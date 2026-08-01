"""Analysis Engine strength context model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engines.analysis_engine.context.interfaces import ContextInterface


@dataclass(slots=True)
class StrengthContext(ContextInterface):
    """Public contract for strength analysis context."""

    id: str
    chart_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)

    def context_id(self) -> str:
        """Return the context identifier."""
        raise NotImplementedError

    def get(self, key: str) -> Any:
        """Return a context value by key."""
        raise NotImplementedError

    def set(self, key: str, value: Any) -> None:
        """Assign a context value by key."""
        raise NotImplementedError
