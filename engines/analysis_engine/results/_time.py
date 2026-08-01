"""Shared timestamp helper for result infrastructure."""

from __future__ import annotations

from datetime import datetime, timezone


def utc_now() -> str:
    """Return a UTC ISO-8601 timestamp for result infrastructure events."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
