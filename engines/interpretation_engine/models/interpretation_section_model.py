"""Immutable interpretation section architecture model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class InterpretationSectionModel:
    """Architecture section contract. No sentence content hard-coding."""

    id: str
    section_type: str
    title_ref: str | None = None
    content_refs: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate structural section contract."""
        return bool(self.id and self.section_type)
