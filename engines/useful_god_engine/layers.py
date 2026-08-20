"""Semantic layers for Useful God V2: Overall vs Điều hậu."""

from __future__ import annotations

CLIMATE_GROUPS: frozenset[str] = frozenset({"season", "temperature"})
STRUCTURAL_GROUPS: frozenset[str] = frozenset({"strength", "flow", "special"})

OVERALL_INCOMPLETE_MESSAGE = "Chưa đủ căn cứ xác định Dụng thần tổng thể"


def candidate_layer(rule_group: str | None) -> str | None:
    """Return ``overall`` or ``climate`` for a matcher group, else None."""
    group = str(rule_group or "").strip()
    if group in STRUCTURAL_GROUPS:
        return "overall"
    if group in CLIMATE_GROUPS:
        return "climate"
    return None
