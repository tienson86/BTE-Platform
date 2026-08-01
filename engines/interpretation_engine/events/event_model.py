"""Runtime event payload models for Pack 03 Event Bus.

Infrastructure only. No BaZi logic. No external broker.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

from engines.interpretation_engine.events.event_types import InterpretationEventType
from engines.interpretation_engine.runtime.contracts import HealthStatus


def _utc_now() -> str:
    """Return UTC ISO-8601 timestamp."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(frozen=True, slots=True)
class RuntimeEvent:
    """Immutable local runtime event envelope."""

    event_type: InterpretationEventType
    source: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    event_id: str = ""
    timestamp: str = ""
    correlation_id: str | None = None

    def validate(self) -> bool:
        """Validate event envelope structural integrity."""
        if not isinstance(self.event_type, InterpretationEventType):
            return False
        return bool(self.source)


def make_event(
    event_type: InterpretationEventType,
    *,
    source: str,
    payload: Mapping[str, Any] | None = None,
    correlation_id: str | None = None,
    event_id: str | None = None,
) -> RuntimeEvent:
    """Build a RuntimeEvent with timestamp defaults."""
    stamp = _utc_now()
    return RuntimeEvent(
        event_type=event_type,
        source=source,
        payload=dict(payload or {}),
        event_id=event_id or f"evt_{event_type.value}_{stamp}",
        timestamp=stamp,
        correlation_id=correlation_id,
    )


def health_changed_payload(
    *,
    previous: HealthStatus | str | None,
    current: HealthStatus | str,
    runtime_id: str,
) -> dict[str, Any]:
    """Build a health_changed payload."""
    prev_value = previous.value if isinstance(previous, HealthStatus) else previous
    curr_value = current.value if isinstance(current, HealthStatus) else current
    return {
        "runtime_id": runtime_id,
        "previous": prev_value,
        "current": curr_value,
    }
