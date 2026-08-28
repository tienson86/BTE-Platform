"""Canonical Four Pillars month Ganzhi: 12 Tiết + Ngũ Hổ Độn.

Standard
    BTE-MONTH-PILLAR-SOLAR-TERM-V1.0

Supersedes
    BTE-MONTH-PILLAR-LUNAR-V1.0

Month branch comes from solar-term nguyệt lệnh (Lập Xuân = Dần, … Lập Thu = Thân).
Month stem comes from the year-pillar stem via Ngũ Hổ Độn.

Does not use lunar month number. Does not compute day or hour Ganzhi.
"""

from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path

from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.calendar_engine.solar_terms.engine import SolarTermEngine, SolarTermMonth

MONTH_PILLAR_STANDARD = "BTE-MONTH-PILLAR-SOLAR-TERM-V1.0"

STEMS: tuple[str, ...] = tuple(GanzhiAlgorithm.STEM)
BRANCHES_DAN_FIRST: tuple[str, ...] = (
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

_RULES_CSV = (
    Path(__file__).resolve().parent / "solar_terms" / "data" / "month_stem_rules.csv"
)


@lru_cache(maxsize=1)
def yin_start_stem_index() -> dict[str, int]:
    """Ngũ Hổ Độn: Thiên Can index of tháng Dần for each year stem."""
    with _RULES_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    mapping: dict[str, int] = {}
    for row in rows:
        stem = (row.get("year_stem") or "").strip()
        index = int(row["start_month_stem_index"])
        if stem:
            mapping[stem] = index
    if len(mapping) != 10:
        raise ValueError(f"month_stem_rules.csv must cover 10 year stems, got {len(mapping)}")
    return mapping


def month_stem_for(year_stem: str, month_index: int) -> str:
    """Thiên Can tháng. ``month_index`` 1 = Dần … 12 = Sửu."""
    if month_index < 1 or month_index > 12:
        raise ValueError(f"month_index must be 1–12, got {month_index}")
    start = yin_start_stem_index()[year_stem]
    return STEMS[(start + month_index - 1) % 10]


def bazi_year_number(year: int, month: int, day: int, terms: SolarTermEngine) -> int:
    """Year pillar year. Changes at Lập Xuân, not Tết."""
    if terms.is_after_li_chun(year, month, day):
        return year
    return year - 1


def solar_term_month(
    year: int,
    month: int,
    day: int,
    terms: SolarTermEngine | None = None,
) -> SolarTermMonth:
    """Nguyệt lệnh from 12 Tiết."""
    engine = terms or SolarTermEngine()
    return engine.get_bazi_month(year, month, day)


def month_pillar(
    year: int,
    month: int,
    day: int,
    terms: SolarTermEngine | None = None,
) -> tuple[str, str]:
    """Return ``(stem, branch)`` for the Four Pillars month at a Gregorian date."""
    engine = terms or SolarTermEngine()
    info = engine.get_bazi_month(year, month, day)
    year_stem = GanzhiAlgorithm.year(bazi_year_number(year, month, day, engine))["can"]
    stem = month_stem_for(year_stem, info.month_index)
    return stem, info.branch


def month_ganzhi_label(
    year: int,
    month: int,
    day: int,
    terms: SolarTermEngine | None = None,
) -> str:
    """``Can Chi`` label, e.g. ``Bính Thân``."""
    stem, branch = month_pillar(year, month, day, terms=terms)
    return f"{stem} {branch}"
