"""Append-only release event types. No personal data."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

EVENT_RUNTIME = "runtime"
EVENT_PRESENTATION = "presentation"
EVENT_PROVIDER = "provider_change"
EVENT_FALLBACK_AUTO = "automatic_fallback"
EVENT_FALLBACK_MANUAL = "manual_rollback"
EVENT_PARITY = "parity"
EVENT_GOLDEN = "golden"
EVENT_HEALTH = "health"

ALLOWED_EVENTS: frozenset[str] = frozenset(
    {
        EVENT_RUNTIME,
        EVENT_PRESENTATION,
        EVENT_PROVIDER,
        EVENT_FALLBACK_AUTO,
        EVENT_FALLBACK_MANUAL,
        EVENT_PARITY,
        EVENT_GOLDEN,
        EVENT_HEALTH,
    }
)

ALLOWED_PROVIDERS: frozenset[str] = frozenset({"pack05", "v2", "auto"})


@dataclass(frozen=True, slots=True)
class ReleaseEvent:
    """Operational event. Never stores names, birth data, or narrative text."""

    event: str
    time: str
    provider: str
    status: str
    reason: str

    def to_record(self) -> dict[str, Any]:
        """JSON-safe row."""
        return {
            "event": self.event,
            "time": self.time,
            "provider": self.provider,
            "status": self.status,
            "reason": self.reason,
        }

    @classmethod
    def from_record(cls, row: Mapping[str, Any]) -> "ReleaseEvent":
        """Hydrate one history row."""
        return cls(
            event=str(row.get("event") or ""),
            time=str(row.get("time") or ""),
            provider=str(row.get("provider") or ""),
            status=str(row.get("status") or ""),
            reason=str(row.get("reason") or ""),
        )


def utc_now() -> str:
    """UTC timestamp without microseconds."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def make_event(
    event: str,
    *,
    provider: str,
    status: str,
    reason: str = "",
    time: str | None = None,
) -> ReleaseEvent:
    """Build a release event. Drops unknown event names to a generic health row."""
    name = event if event in ALLOWED_EVENTS else EVENT_HEALTH
    next_provider = provider if provider in ALLOWED_PROVIDERS else "v2"
    return ReleaseEvent(
        event=name,
        time=time or utc_now(),
        provider=next_provider,
        status=status,
        reason=reason,
    )
