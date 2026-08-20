"""
Shared helpers for Luck runtime providers (Sprint 4.1).

Pillar enrichment and calendar conversion only — no luck evaluation.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from engines.bazi_engine.ten_god import STEM_META, branch_element, ten_god_name
from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.calendar_engine.julian.julian import JulianDay
from engines.calendar_engine.solar_terms.engine import SolarTermEngine
from engines.luck_engine.exceptions import LuckContextError
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
# V1.0 lock (G1-08 Option A): integer start age, calendar-day 12-Jie, year-level current.
PRECISION_LEVEL = "year_level"
START_AGE_METHOD = "major_jie_days_div_3"
CURRENT_AGE_BASIS = "current_year - birth_year"
METHOD_NOTE_VI = "Khởi vận theo ngày lịch và Tiết khí, độ chính xác theo năm"
DIRECTION_LABELS: dict[str, str] = {"forward": "Thuận", "reverse": "Nghịch"}
GENDER_LABELS: dict[str, str] = {"male": "Nam", "female": "Nữ"}
_MALE_GENDER_ALIASES = frozenset({"male", "nam", "m", "1", "man", "boy"})
_FEMALE_GENDER_ALIASES = frozenset({"female", "nu", "nữ", "f", "woman", "girl"})


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
    LuckContextError
        When gender is missing or unsupported.
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
    if year is None or month is None or day is None:
        raise ValueError("calendar must expose solar year/month/day")
    gender = normalize_luck_gender(getattr(bazi, "gender", None))
    return int(year), int(month), int(day), hour, minute, gender


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


def normalize_luck_gender(gender: Any) -> str:
    """
    Return canonical ``male`` / ``female``.

    Raises LuckContextError when gender is missing or unsupported.
    Does not default missing gender to male.
    """
    if gender is None:
        raise LuckContextError("gender_required")
    value = str(gender).strip()
    if not value:
        raise LuckContextError("gender_required")
    key = value.lower()
    if key in _MALE_GENDER_ALIASES:
        return "male"
    if key in _FEMALE_GENDER_ALIASES:
        return "female"
    raise LuckContextError(f"unsupported_gender:{value}")


def gender_display_label(gender: Any) -> str:
    """Customer-facing Nam/Nữ. Empty when gender is missing or invalid."""
    try:
        return GENDER_LABELS[normalize_luck_gender(gender)]
    except LuckContextError:
        return ""


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
    """True when gender normalizes to male. Invalid gender raises."""
    return normalize_luck_gender(gender) == "male"


def dayun_forward(gender: str, year_stem: str) -> bool:
    """
    V1.0 DaYun direction (G1-08).

    ``is_male(gender) == is_yang(year_stem)`` → thuận / forward.
    Polarity is Niên can via STEM_META, never Nhật can.
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
        "branch_element": branch_element(branch),
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
    V1.0 start age from calendar days to the adjacent 12-Jie (Tiết).

    Formula (locked): ``start_age = max(1, round(days / 3))``.
    Birth hour/minute is not used. Same civil day as a Jie is neither
    before nor after that Jie (V1.0 has no Jie timestamp).
    """
    engine = terms or SolarTermEngine()
    birth = date(birth_year, birth_month, birth_day)
    before: list[tuple[date, int]] = []
    after: list[tuple[date, int]] = []
    same_day: list[str] = []
    names = getattr(engine, "_names", ())
    for year in (birth_year - 1, birth_year, birth_year + 1):
        for term_index in engine._MONTH_START_TERM_INDEX:
            yy, mm, dd = engine.get_term_datetime_parts(year, term_index)
            term_date = date(yy, mm, dd)
            jie_name = names[term_index] if term_index < len(names) else str(term_index)
            if term_date < birth:
                before.append((term_date, term_index))
            elif term_date > birth:
                after.append((term_date, term_index))
            else:
                same_day.append(f"{jie_name} {term_date.isoformat()}")
    if forward:
        if not after:
            raise ValueError("no forward Tiết found for Dayun start age")
        anchor, anchor_index = min(after, key=lambda item: item[0])
        days = (anchor - birth).days
    else:
        if not before:
            raise ValueError("no reverse Tiết found for Dayun start age")
        anchor, anchor_index = max(before, key=lambda item: item[0])
        days = (birth - anchor).days
    start_age = max(1, int(round(days / DAYS_PER_START_AGE_YEAR)))
    anchor_name = names[anchor_index] if anchor_index < len(names) else ""
    return start_age, {
        "method": START_AGE_METHOD,
        "direction": "forward" if forward else "reverse",
        "days_to_jie": days,
        "anchor_jie_date": anchor.isoformat(),
        "anchor_jie_name": anchor_name,
        "days_per_year": DAYS_PER_START_AGE_YEAR,
        "precision": PRECISION_LEVEL,
        "jie_set": "month_start_12_jie",
        "hour_used": False,
        "same_day_jie_skipped": same_day,
        "same_day_jie_limitation": (
            "V1.0 date-level Jie cannot order birth on the same civil day; "
            "that Jie is skipped."
            if same_day
            else ""
        ),
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
