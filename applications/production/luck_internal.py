"""Internal luck sequence extraction — not exposed in Customer Mode."""

from __future__ import annotations

from typing import Any


def extract_internal_dayun_sequence(luck: dict[str, Any]) -> list[dict[str, Any]]:
    """Return full DaYun sequence from current_dayun.metadata.sequence."""
    if not luck:
        return []
    current = luck.get("current_dayun")
    if not isinstance(current, dict):
        return []
    metadata = current.get("metadata") or {}
    sequence = metadata.get("sequence")
    if isinstance(sequence, list):
        return [item for item in sequence if isinstance(item, dict)]
    return []
