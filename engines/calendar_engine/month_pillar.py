"""Lunar-calendar month Ganzhi helper.

Four Pillars / BaZi month Ganzhi is NOT derived here.
Canonical BaZi month identity remains ``engines.calendar_engine.month_ganzhi``
(BTE-MONTH-PILLAR-SOLAR-TERM-V1.0) and still changes at Jie Qi.

This module owns lunar-month display identity only:
lunar month number → branch, Ngũ Hổ Độn from the *lunar year* stem.
Leap months keep the same month number and therefore the same Can Chi.
"""

from __future__ import annotations

from engines.calendar_engine.month_ganzhi import MONTH_PILLAR_STANDARD, month_stem_for

__all__ = (
    "LUNAR_MONTH_BRANCHES",
    "MONTH_PILLAR_STANDARD",
    "lunar_month_ganzhi",
    "lunar_month_to_branch",
)

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


def lunar_month_ganzhi(lunar_year_stem: str, lunar_month: int) -> str:
    """Can Chi of the lunar calendar month.

    Branch follows lunar month number (1 = Dần … 12 = Sửu).
    Stem is Ngũ Hổ Độn from the lunar-year stem — never the BaZi month pillar.
    """
    stem = (lunar_year_stem or "").strip()
    if not stem:
        raise ValueError("lunar year stem is required")
    branch = lunar_month_to_branch(lunar_month)
    return f"{month_stem_for(stem, int(lunar_month))} {branch}"
