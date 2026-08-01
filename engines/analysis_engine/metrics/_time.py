"""Shared helpers for metrics infrastructure."""

from __future__ import annotations

from datetime import datetime, timezone
from time import perf_counter


def utc_now() -> str:
    """Return a UTC ISO-8601 timestamp for metrics infrastructure."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Stopwatch:
    """Simple monotonic stopwatch for infrastructure timing."""

    def __init__(self) -> None:
        """Initialize an unstarted stopwatch."""
        self._started_at: float | None = None
        self._elapsed_ms: float | None = None

    def start(self) -> None:
        """Start or restart the stopwatch."""
        self._started_at = perf_counter()
        self._elapsed_ms = None

    def stop(self) -> float:
        """Stop the stopwatch and return elapsed milliseconds."""
        if self._started_at is None:
            return 0.0
        self._elapsed_ms = (perf_counter() - self._started_at) * 1000.0
        self._started_at = None
        return self._elapsed_ms

    @property
    def elapsed_ms(self) -> float | None:
        """Return elapsed milliseconds if stopped, else None."""
        return self._elapsed_ms
