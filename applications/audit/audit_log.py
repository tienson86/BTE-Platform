"""Audit log store (in-memory + optional JSON append)."""

from __future__ import annotations

import json
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(slots=True)
class AuditEvent:
    """One auditable activity."""

    event_id: str
    event_type: str
    created_at: str
    actor_id: str | None = None
    actor_username: str | None = None
    resource: str | None = None
    detail: dict[str, Any] = field(default_factory=dict)
    status_code: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize event."""
        return asdict(self)


class AuditLog:
    """Thread-safe audit event buffer."""

    def __init__(self, *, max_events: int = 5000, persist_path: Path | str | None = None) -> None:
        self.max_events = max_events
        self.persist_path = Path(persist_path) if persist_path else None
        self._events: list[AuditEvent] = []
        self._lock = threading.Lock()

    def append(self, event: AuditEvent) -> AuditEvent:
        """Append an event (newest last)."""
        with self._lock:
            self._events.append(event)
            if len(self._events) > self.max_events:
                self._events = self._events[-self.max_events :]
            if self.persist_path is not None:
                self.persist_path.parent.mkdir(parents=True, exist_ok=True)
                with self.persist_path.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
        return event

    def list(
        self,
        *,
        limit: int = 100,
        event_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return newest events first."""
        with self._lock:
            items = list(self._events)
        if event_type:
            items = [e for e in items if e.event_type == event_type]
        items.reverse()
        return [e.to_dict() for e in items[: max(limit, 1)]]

    def clear(self) -> None:
        """Clear buffer (tests)."""
        with self._lock:
            self._events.clear()

    def create(
        self,
        event_type: str,
        *,
        actor_id: str | None = None,
        actor_username: str | None = None,
        resource: str | None = None,
        detail: dict[str, Any] | None = None,
        status_code: int | None = None,
    ) -> AuditEvent:
        """Create and store an audit event."""
        event = AuditEvent(
            event_id=str(uuid4()),
            event_type=event_type,
            created_at=_utcnow(),
            actor_id=actor_id,
            actor_username=actor_username,
            resource=resource,
            detail=dict(detail or {}),
            status_code=status_code,
        )
        return self.append(event)


_AUDIT = AuditLog()


def get_audit_log() -> AuditLog:
    """Process-wide audit log."""
    return _AUDIT
