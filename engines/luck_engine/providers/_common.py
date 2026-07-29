"""
Shared helpers for Luck runtime providers (Sprint 4.1).

Pillar enrichment and calendar conversion only — no luck evaluation.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from engines.bazi_engine.ten_god import STEM_META, ten_god_name
from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.calendar_engine.julian.julian import JulianDay
from engines.calendar_engine.solar_terms.engine import SolarTermEngine
from engines.rule_contract.signal_maps import BRANCH_HIDDEN

STEMS: tuple[str, ...] = tuple(GanzhiAlgorithm.STEM)
BRANCHES: tuple[str, ...] = tuple(GanzhiAlgorithm.BRANCH)

# Ngũ Hổ Độn: stem index of month Dần for each year stem.
MONTH_YIN_START_STEM: dict[str, int] = {
    "Giáp": 2,
    "Kỷ": 2,
    "Ất": 4,
    "Canh": 4,
    "Bính": 6,
    "Tân": 6,
    "Đinh": 8,
    "Nhâm": 8,
    "Mậu": 0,
    "Quý": 0,
}

DAYUN_COUNT = 10
DAYS_PER_START_AGE_YEAR = 3.0


def extract_birth_parts(
    calendar: Any,
    bazi: Any,
) -> tuple[int, int, int, int, int, str]:
    """
    Resolve birth solar Y-M-D H:M and gender from calendar / BaZi inputs.

    Raises
    ------
    ValueError
        When required birth fields are missing.
    """
    year = getattr(calendar, "solar_year", None)
    month = getattr(calendar, "solar_month", None)
    day = getattr(calendar, "solar_day", None)
    hour = int(getattr(calendar, "solar_hour", 0) or 0)
    minute = int(getattr(calendar, "solar_minute", 0) or 0)
    if year is None or month is None or day is None:
        solar = getattr(calendar, "solar", None)
        year = getattr(solar, "year", year)
        month = getattr(solar, "month", month)
        day = getattr(solar, "day", day)
    gender = getattr(bazi, "gender", None) or "male"
    if year is None or month is None or day is None:
        raise ValueError("calendar must expose solar year/month/day")
    return int(year), int(month), int(day), hour, minute, str(gender)


def day_master_of(bazi: Any) -> str:
    """Return Nhật Chủ stem from BaZi chart."""
    dm = getattr(bazi, "day_master", None)
    if dm:
        return str(dm)
    day_pillar = getattr(bazi, "day_pillar", None)
    stem = getattr(day_pillar, "stem", None)
    if not stem:
        raise ValueError("bazi must expose day_master or day_pillar.stem")
    return str(stem)


def stem_element(stem: str) -> str:
    """Ngũ hành of a heavenly stem."""
    meta = STEM_META.get(stem)
    return meta[0] if meta else ""


def stem_yin_yang(stem: str) -> str:
    """Âm/Dương of a heavenly stem."""
    meta = STEM_META.get(stem)
    return meta[1] if meta else ""


def hidden_stems_of(branch: str) -> tuple[str, ...]:
    """Tàng can of an earthly branch."""
    return tuple(BRANCH_HIDDEN.get(branch, []))


def jiazi_index(stem: str, branch: str) -> int:
    """Index 0..59 of a Can Chi pair in the sexagenary cycle."""
    for index in range(60):
        if STEMS[index % 10] == stem and BRANCHES[index % 12] == branch:
            return index
    raise ValueError(f"unknown ganzhi pair: {stem} {branch}")


def step_jiazi(stem: str, branch: str, step: int) -> tuple[str, str]:
    """Move ``step`` places along the 60-jiazi cycle."""
    index = (jiazi_index(stem, branch) + step) % 60
    return STEMS[index % 10], BRANCHES[index % 12]


def is_yang_stem(stem: str) -> bool:
    """True when stem polarity is Dương."""
    return stem_yin_yang(stem) == "Dương"


def is_male_gender(gender: str) -> bool:
    """Normalize gender labels to male/female."""
    value = gender.strip().lower()
    return value in {"male", "nam", "m", "1"}


def dayun_forward(gender: str, year_stem: str) -> bool:
    """
    Classical DaYun direction.

    Male + yang year stem / female + yin year stem → forward.
    """
    return is_male_gender(gender) == is_yang_stem(year_stem)


def bazi_year_of(year: int, month: int, day: int, terms: SolarTermEngine) -> int:
    """Year pillar year (changes at Lập Xuân)."""
    if terms.is_after_li_chun(year, month, day):
        return year
    return year - 1


def month_stem_for(year_stem: str, month_index: int) -> str:
    """Thiên Can tháng via Ngũ Hổ Độn (month_index 1 = Dần)."""
    start = MONTH_YIN_START_STEM[year_stem]
    return STEMS[(start + month_index - 1) % 10]


def hour_pillar_for(day_stem: str, hour: int) -> tuple[str, str]:
    """Hour Can Chi via Ngũ Thử Độn."""
    if hour >= 23 or hour < 1:
        branch_index = 0
    else:
        branch_index = ((hour + 1) // 2) % 12
    stem_index = (STEMS.index(day_stem) * 2 + branch_index) % 10
    return STEMS[stem_index], BRANCHES[branch_index]


def year_ganzhi(year: int) -> tuple[str, str]:
    """Year stem/branch for a BaZi year number."""
    payload = GanzhiAlgorithm.year(year)
    return payload["can"], payload["chi"]


def day_ganzhi(year: int, month: int, day: int) -> tuple[str, str]:
    """Day stem/branch from Gregorian date."""
    jdn = JulianDay.day_number(year, month, day)
    payload = GanzhiAlgorithm.day(jdn)
    return payload["can"], payload["chi"]


def enrich_stem(
    stem: str,
    branch: str,
    day_master: str,
) -> dict[str, Any]:
    """Build shared pillar enrichment fields (no evaluation)."""
    return {
        "heavenly_stem": stem,
        "earthly_branch": branch,
        "ganzhi": f"{stem} {branch}",
        "element": stem_element(stem),
        "yin_yang": stem_yin_yang(stem),
        "ten_god": ten_god_name(day_master, stem),
        "hidden_stems": hidden_stems_of(branch),
    }


def compute_dayun_start_age(
    birth_year: int,
    birth_month: int,
    birth_day: int,
    *,
    forward: bool,
    terms: SolarTermEngine | None = None,
) -> tuple[int, dict[str, Any]]:
    """
    Start age from days to adjacent major Tiết (3 days ≈ 1 year).

    Returns
    -------
    tuple[int, dict]
        (start_age, calculation metadata)
    """
    engine = terms or SolarTermEngine()
    birth = date(birth_year, birth_month, birth_day)
    before: list[date] = []
    after: list[date] = []
    for year in (birth_year - 1, birth_year, birth_year + 1):
        for term_index in engine._MONTH_START_TERM_INDEX:
            yy, mm, dd = engine.get_term_datetime_parts(year, term_index)
            term_date = date(yy, mm, dd)
            if term_date < birth:
                before.append(term_date)
            elif term_date > birth:
                after.append(term_date)
    if forward:
        if not after:
            raise ValueError("no forward Tiết found for Dayun start age")
        anchor = min(after)
        days = (anchor - birth).days
    else:
        if not before:
            raise ValueError("no reverse Tiết found for Dayun start age")
        anchor = max(before)
        days = (birth - anchor).days
    start_age = max(1, int(round(days / DAYS_PER_START_AGE_YEAR)))
    return start_age, {
        "method": "major_jie_days_div_3",
        "direction": "forward" if forward else "reverse",
        "days_to_jie": days,
        "anchor_jie_date": anchor.isoformat(),
        "days_per_year": DAYS_PER_START_AGE_YEAR,
    }


def resolve_reference_dt(
    calendar: Any,
    reference_dt: datetime | None,
) -> datetime:
    """
    Reference instant for current Liunian / Liuyue / Liuri / Liushi.

    Defaults to ``datetime.now()`` when not injected (runtime “now”).
    """
    if reference_dt is not None:
        return reference_dt
    del calendar
    return datetime.now()
