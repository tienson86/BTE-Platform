"""Output artifact architecture model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class OutputArtifact:
    """Immutable output artifact shell."""

    id: str
    format_id: str
    source_result_id: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate artifact structural contract."""
        return bool(self.id and self.format_id and self.source_result_id)
