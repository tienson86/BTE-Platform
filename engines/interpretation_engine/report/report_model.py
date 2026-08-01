"""Report architecture model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class InterpretationReportModel:
    """Immutable report shell. No hard-coded narrative content."""

    id: str
    source_result_id: str
    section_refs: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate report structural contract."""
        return bool(self.id and self.source_result_id)
