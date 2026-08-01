"""Analysis metadata and shared timestamp contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class ModelTimestamps:
    """Immutable timestamp contract for analysis models."""

    created_at: str
    updated_at: str | None = None
    completed_at: str | None = None


@dataclass(frozen=True, slots=True)
class AnalysisMetadata:
    """Immutable metadata contract for analysis models."""

    id: str
    version: str
    metadata: Mapping[str, Any] = field(default_factory=dict)
    trace: tuple[str, ...] = ()
    timestamps: ModelTimestamps | None = None

    def validate(self) -> bool:
        """Validate metadata contract."""
        raise NotImplementedError
