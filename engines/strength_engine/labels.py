"""Canonical V1.0 Strength class labels. Taxonomy is three classes only."""

from __future__ import annotations

STRENGTH_LEVEL_LABELS: dict[str, str] = {
    "weak": "Thân nhược",
    "balanced": "Thân cân bằng",
    "strong": "Thân vượng",
}


def strength_level_label(level: str | None) -> str:
    """Map internal strength_level to the V1.0 Vietnamese label."""
    key = str(level or "").strip().lower()
    return STRENGTH_LEVEL_LABELS.get(key, "")
