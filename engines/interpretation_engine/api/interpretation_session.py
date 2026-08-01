"""Interpretation session contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class InterpretationSessionStatus(str, Enum):
    """Session lifecycle status."""

    OPEN = "open"
    CLOSED = "closed"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class InterpretationSession:
    """Session contract for Pack 03 API facade."""

    id: str
    pipeline_id: str
    status: InterpretationSessionStatus = InterpretationSessionStatus.OPEN
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate session structural contract."""
        return bool(self.id and self.pipeline_id)
