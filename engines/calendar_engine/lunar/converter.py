"""
Vietnamese solar ↔ lunar conversion (Hồ Ngọc Đức algorithm).

Timezone default: UTC+7 (Vietnam).
Supported range: approximately 1900–2100.
"""

from __future__ import annotations

import math
from typing import NamedTuple


class LunarParts(NamedTuple):
    """Lunar Y/M/D with leap-month flag."""

    day: int
    month: int
    year: int
    leap: bool


def _floor(value: float) -> int:
    return int(math.floor(value))


def jd_from_date(day: int, month: int, year: int) -> int:
    """Gregorian (or Julian before 1582-10-15) date → Julian Day Number."""
    a = _floor((14 - month) / 12)
    y = year + 4800 - a
    m = month + 12 * a - 3
    jd = day + _floor((153 * m + 2) / 5) + 365 * y + _floor(y / 4) - _floor(y / 100) + _floor(
        y / 400
    ) - 32045
    if jd < 2299161:
        jd = day + _floor((153 * m + 2) / 5) + 365 * y + _floor(y / 4) - 32083
    return jd


def _new_moon(k: float) -> float:
    """Approximate Julian date of the k-th new moon after 1900-01-01."""
    t = k / 1236.85
    t2 = t * t
    t3 = t2 * t
    dr = math.pi / 180.0
    jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * t2 - 0.000000155 * t3
    jd1 = jd1 + 0.00033 * math.sin((166.56 + 132.87 * t - 0.009173 * t2) * dr)
    m = 359.2242 + 29.10535608 * k - 0.0000333 * t2 - 0.00000347 * t3
    mpr = 306.0253 + 385.81691806 * k + 0.0107306 * t2 + 0.00001236 * t3
    f = 21.2964 + 390.67050646 * k - 0.0016528 * t2 - 0.00000239 * t3
    c1 = (0.1734 - 0.000393 * t) * math.sin(m * dr) + 0.0021 * math.sin(2 * dr * m)
    c1 = c1 - 0.4068 * math.sin(mpr * dr) + 0.0161 * math.sin(dr * 2 * mpr)
    c1 = c1 - 0.0004 * math.sin(dr * 3 * mpr)
    c1 = c1 + 0.0104 * math.sin(dr * 2 * f) - 0.0051 * math.sin(dr * (m + mpr))
    c1 = c1 - 0.0074 * math.sin(dr * (m - mpr)) + 0.0004 * math.sin(dr * (2 * f + m))
    c1 = c1 - 0.0004 * math.sin(dr * (2 * f - m)) - 0.0006 * math.sin(dr * (2 * f + mpr))
    c1 = c1 + 0.0010 * math.sin(dr * (2 * f - mpr)) + 0.0005 * math.sin(dr * (2 * mpr + m))
    if t < -11:
        deltat = 0.001 + 0.000839 * t + 0.0002261 * t2 - 0.00000845 * t3 - 0.000000081 * t * t3
    else:
        deltat = -0.000278 + 0.000265 * t + 0.000262 * t2
    return jd1 + c1 - deltat


def _sun_longitude(jdn: float) -> float:
    """True solar longitude in radians, normalized to [0, 2π)."""
    t = (jdn - 2451545.0) / 36525.0
    t2 = t * t
    dr = math.pi / 180.0
    m = 357.52910 + 35999.05030 * t - 0.0001559 * t2 - 0.00000048 * t * t2
    l0 = 280.46645 + 36000.76983 * t + 0.0003032 * t2
    dl = (1.914600 - 0.004817 * t - 0.000014 * t2) * math.sin(dr * m)
    dl = dl + (0.019993 - 0.000101 * t) * math.sin(dr * 2 * m) + 0.000290 * math.sin(dr * 3 * m)
    longitude = (l0 + dl) * dr
    return longitude - math.pi * 2 * _floor(longitude / (math.pi * 2))


def _get_new_moon_day(k: int, time_zone: float) -> int:
    return _floor(_new_moon(k) + 0.5 + time_zone / 24.0)


def _get_sun_longitude_sector(day_number: int, time_zone: float) -> int:
    return _floor(_sun_longitude(day_number - 0.5 - time_zone / 24.0) / math.pi * 6)


def _get_lunar_month11(year: int, time_zone: float) -> int:
    off = jd_from_date(31, 12, year) - 2415021
    k = _floor(off / 29.530588853)
    nm = _get_new_moon_day(k, time_zone)
    sun_long = _get_sun_longitude_sector(nm, time_zone)
    if sun_long >= 9:
        nm = _get_new_moon_day(k - 1, time_zone)
    return nm


def _get_leap_month_offset(a11: int, time_zone: float) -> int:
    k = _floor((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    last = 0
    i = 1
    arc = _get_sun_longitude_sector(_get_new_moon_day(k + i, time_zone), time_zone)
    while True:
        last = arc
        i += 1
        arc = _get_sun_longitude_sector(_get_new_moon_day(k + i, time_zone), time_zone)
        if arc == last or i >= 14:
            break
    return i - 1


def solar_to_lunar(
    day: int,
    month: int,
    year: int,
    time_zone: float = 7.0,
) -> LunarParts:
    """
    Convert a Gregorian solar date to Vietnamese lunar date.

    Args:
        day: Solar day of month.
        month: Solar month.
        year: Solar year.
        time_zone: UTC offset hours (Vietnam = 7).

    Returns:
        LunarParts with day, month, year, leap.
    """
    day_number = jd_from_date(day, month, year)
    k = _floor((day_number - 2415021.076998695) / 29.530588853)
    month_start = _get_new_moon_day(k + 1, time_zone)
    if month_start > day_number:
        month_start = _get_new_moon_day(k, time_zone)

    a11 = _get_lunar_month11(year, time_zone)
    b11 = a11
    if a11 >= day_number:
        lunar_year = year
        a11 = _get_lunar_month11(year - 1, time_zone)
    else:
        lunar_year = year + 1
        b11 = _get_lunar_month11(year + 1, time_zone)

    lunar_day = day_number - month_start + 1
    diff = _floor((month_start - a11) / 29)
    lunar_leap = False
    lunar_month = diff + 11

    if b11 - a11 > 365:
        leap_month_diff = _get_leap_month_offset(a11, time_zone)
        if diff >= leap_month_diff:
            lunar_month = diff + 10
            if diff == leap_month_diff:
                lunar_leap = True

    if lunar_month > 12:
        lunar_month -= 12
    if lunar_month >= 11 and diff < 4:
        lunar_year -= 1

    return LunarParts(
        day=int(lunar_day),
        month=int(lunar_month),
        year=int(lunar_year),
        leap=bool(lunar_leap),
    )
