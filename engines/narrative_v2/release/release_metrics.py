"""Release counters derived from events. No personal data."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.release.release_events import (
    EVENT_FALLBACK_AUTO,
    EVENT_FALLBACK_MANUAL,
    EVENT_GOLDEN,
    EVENT_PARITY,
    EVENT_PRESENTATION,
    EVENT_PROVIDER,
    EVENT_RUNTIME,
    ReleaseEvent,
)


@dataclass(frozen=True, slots=True)
class ReleaseMetrics:
    """Operational counters for the dual-run window."""

    runtime_success: int
    runtime_failure: int
    presentation_success: int
    presentation_failure: int
    fallback_automatic: int
    fallback_manual: int
    provider_changes: int
    parity_fail: int
    golden_mismatch: int

    @property
    def fallback_count(self) -> int:
        """Automatic plus manual fallback events."""
        return self.fallback_automatic + self.fallback_manual


def metrics_from_events(events: tuple[ReleaseEvent, ...] | list[ReleaseEvent]) -> ReleaseMetrics:
    """Count operational events. Ignores narrative content."""
    runtime_ok = _count(events, EVENT_RUNTIME, "PASS")
    runtime_fail = _count(events, EVENT_RUNTIME, "FAIL")
    pres_ok = _count(events, EVENT_PRESENTATION, "PASS")
    pres_fail = _count(events, EVENT_PRESENTATION, "FAIL")
    auto = sum(1 for row in events if row.event == EVENT_FALLBACK_AUTO)
    manual = sum(1 for row in events if row.event == EVENT_FALLBACK_MANUAL)
    changes = sum(1 for row in events if row.event == EVENT_PROVIDER)
    parity_fail = _count(events, EVENT_PARITY, "FAIL")
    golden_fail = _count(events, EVENT_GOLDEN, "FAIL")
    return ReleaseMetrics(
        runtime_success=runtime_ok,
        runtime_failure=runtime_fail,
        presentation_success=pres_ok,
        presentation_failure=pres_fail,
        fallback_automatic=auto,
        fallback_manual=manual,
        provider_changes=changes,
        parity_fail=parity_fail,
        golden_mismatch=golden_fail,
    )


def _count(events: tuple[ReleaseEvent, ...] | list[ReleaseEvent], event: str, status: str) -> int:
    return sum(1 for row in events if row.event == event and row.status == status)
