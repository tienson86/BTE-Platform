"""Lunar-month branch helper.

Four Pillars month Ganzhi is NOT derived here.
Canonical month identity is ``engines.calendar_engine.month_ganzhi``
(BTE-MONTH-PILLAR-SOLAR-TERM-V1.0).
"""

from __future__ import annotations

from engines.calendar_engine.month_ganzhi import MONTH_PILLAR_STANDARD

# Lunar month number → Địa Chi. Tháng 1 = Dần … tháng 12 = Sửu.
# Kept for lunar-calendar display. Not Four Pillars month identity.
LUNAR_MONTH_BRANCHES: tuple[str, ...] = (
    "Dần",
    "Mão",
    "Thìn",
    "Tỵ",
    "Ngọ",
    "Mùi",
    "Thân",
    "Dậu",
    "Tuất",
    "Hợi",
    "Tý",
    "Sửu",
)


def lunar_month_to_branch(lunar_month: int) -> str:
    """Map lunar month number (1–12) to Địa Chi. Not Four Pillars month Ganzhi."""
    index = int(lunar_month)
    if index < 1 or index > 12:
        raise ValueError(f"lunar month must be 1–12, got {lunar_month}")
    return LUNAR_MONTH_BRANCHES[index - 1]
