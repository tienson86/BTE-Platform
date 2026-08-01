"""Internal Analysis Engine event models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4

from engines.analysis_engine.events.event_types import EventType


def utc_now() -> str:
    """Return a UTC ISO-8601 timestamp for internal event emission."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(frozen=True, slots=True)
class Event:
    """Immutable internal runtime event.

    Carries opaque payload data only. Does not perform analysis or messaging I/O.
    """

    event_id: str
    event_type: EventType
    timestamp: str
    source: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    correlation_id: str | None = None
    pipeline_id: str | None = None
    context_id: str | None = None
    result_id: str | None = None


def create_event(
    event_type: EventType,
    *,
    source: str,
    payload: Mapping[str, Any] | None = None,
    event_id: str | None = None,
    timestamp: str | None = None,
    correlation_id: str | None = None,
    pipeline_id: str | None = None,
    context_id: str | None = None,
    result_id: str | None = None,
) -> Event:
    """Create an immutable internal runtime event."""
    return Event(
        event_id=event_id or str(uuid4()),
        event_type=event_type,
        timestamp=timestamp or utc_now(),
        source=source,
        payload=dict(payload or {}),
        correlation_id=correlation_id,
        pipeline_id=pipeline_id,
        context_id=context_id,
        result_id=result_id,
    )
