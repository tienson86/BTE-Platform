"""Overall operational status contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

HealthLevel = Literal["healthy", "degraded", "unhealthy", "unknown"]


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class ComponentStatus:
    """Status of one operational component. No probe execution."""

    name: str
    level: HealthLevel
    kind: Literal["service", "pipeline", "dependency"]
    detail: str = ""


@dataclass(slots=True)
class OperationsStatus:
    """Aggregated operational status snapshot (contract only)."""

    overall: HealthLevel
    components: tuple[ComponentStatus, ...] = field(default_factory=tuple)
    checked_at: datetime = field(default_factory=utc_now)

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-safe status payload."""
        return {
            "overall": self.overall,
            "checked_at": self.checked_at.isoformat(),
            "components": [
                {
                    "name": item.name,
                    "level": item.level,
                    "kind": item.kind,
                    "detail": item.detail,
                }
                for item in self.components
            ],
        }
