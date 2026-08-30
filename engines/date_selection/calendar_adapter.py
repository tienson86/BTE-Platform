"""Adapt canonical Calendar Engine output for Date Selection."""

from __future__ import annotations

from datetime import date, datetime

from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.calendar_engine.engine import CalendarEngine
from engines.calendar_engine.julian.julian import JulianDay
from engines.date_selection.constants import BRANCH_INDEX
from engines.date_selection.exceptions import DateSelectionValidationError
from engines.date_selection.models import CalendarSnapshot

_ENGINE = CalendarEngine()


def _weekday(year: int, month: int, day: int) -> int:
    return date(year, month, day).weekday()


def _split_ganzhi(label: str | None) -> tuple[str, str]:
    text = " ".join((label or "").split())
    parts = text.split(" ", 1)
    if len(parts) != 2:
        raise DateSelectionValidationError(f"invalid Ganzhi: {label!r}")
    return parts[0], parts[1]


def snapshot_for_solar(
    year: int,
    month: int,
    day: int,
    *,
    hour: int = 0,
    minute: int = 0,
    engine: CalendarEngine | None = None,
) -> CalendarSnapshot:
    """Convert a Gregorian civil date through the canonical Calendar Engine."""
    try:
        datetime(year, month, day, hour, minute)
    except ValueError as exc:
        raise DateSelectionValidationError(str(exc)) from exc
    calendar = (engine or _ENGINE).build(year, month, day, hour, minute)
    year_ganzhi = calendar.lunar.year_can_chi or ""
    if not year_ganzhi:
        gz = GanzhiAlgorithm.year(calendar.lunar_year)
        year_ganzhi = f"{gz['can']} {gz['chi']}"
    _, year_branch = _split_ganzhi(year_ganzhi)
    if year_branch not in BRANCH_INDEX:
        raise DateSelectionValidationError(f"unknown year branch: {year_branch!r}")
    # Integer noon JDN (Hồ Ngọc Đức / BaziEngine), not astronomical JD at 00:00 UTC.
    # CalendarResult.julian_day is N.5 and must not be fed to GanzhiAlgorithm.day().
    jdn = JulianDay.day_number(year, month, day)
    day_gz = GanzhiAlgorithm.day(jdn)
    day_ganzhi = f"{day_gz['can']} {day_gz['chi']}"
    lunar_month = int(calendar.lunar_month or 0)
    if lunar_month < 1 or lunar_month > 12:
        raise DateSelectionValidationError(f"invalid lunar month: {lunar_month}")
    month_ganzhi = calendar.month_can_chi or ""
    if not month_ganzhi:
        raise DateSelectionValidationError("calendar month_can_chi is required")
    lunar_leap = bool(calendar.leap_month)
    lunar_label = calendar.lunar_date or ""
    return CalendarSnapshot(
        solar_year=year,
        solar_month=month,
        solar_day=day,
        solar_label=calendar.solar_date or f"{day:02d}/{month:02d}/{year:04d}",
        lunar_year=int(calendar.lunar_year or 0),
        lunar_month=int(calendar.lunar_month or 0),
        lunar_day=int(calendar.lunar_day or 0),
        lunar_leap=lunar_leap,
        lunar_label=lunar_label,
        year_ganzhi=year_ganzhi,
        month_ganzhi=month_ganzhi,
        day_ganzhi=day_ganzhi,
        year_branch=year_branch,
        weekday=_weekday(year, month, day),
        tam_nguyen=calendar.tam_nguyen or "",
        cuu_van=calendar.cuu_van,
    )
