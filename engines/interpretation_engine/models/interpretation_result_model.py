"""Immutable interpretation result architecture model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class InterpretationResultModel:
    """Architecture result contract for Pack 03 outputs."""

    id: str
    version: str
    source_final_result_id: str
    success: bool
    sections: tuple[str, ...] = ()
    explanations: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)
    trace: tuple[str, ...] = ()

    def validate(self) -> bool:
        """Validate structural result contract."""
        if not self.id or not self.version or not self.source_final_result_id:
            return False
        return True
