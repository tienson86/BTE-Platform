"""Canonical Four Pillars Month Branch from lunar month.

Standard
    BTE-MONTH-PILLAR-LUNAR-V1.0

Effective
    2026-08-20

Supersedes
    Four Pillars month from 12 Tiết / SolarTermEngine.get_bazi_month.

Solar terms remain a separate subsystem (season, climate, Luck jie timing).
They must not construct the Four Pillars month pillar.
"""

from __future__ import annotations

MONTH_PILLAR_STANDARD = "BTE-MONTH-PILLAR-LUNAR-V1.0"

# Lunar month number → Địa Chi. Tháng 1 = Dần … tháng 12 = Sửu.
# Leap months keep the same month number, therefore the same branch.
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
    """Map canonical lunar month number (1–12) to the Four Pillars month branch."""
    index = int(lunar_month)
    if index < 1 or index > 12:
        raise ValueError(f"lunar month must be 1–12, got {lunar_month}")
    return LUNAR_MONTH_BRANCHES[index - 1]
