"""
=========================================================
BTE PLATFORM

Calendar Algorithm

File:
    jdn_to_lunar.py

Version:
    1.0

Description:
    Convert Julian Day Number / solar date to Lunar Date
    (delegates to Hồ Ngọc Đức converter).

=========================================================
"""

from engines.calendar_engine.julian.julian import JulianDay
from engines.calendar_engine.lunar.converter import solar_to_lunar


class JDNToLunar:
    """
    Chuyển Julian Day Number / ngày dương sang Âm lịch.
    """

    @staticmethod
    def convert(jdn, timezone=7):
        year, month, day = JulianDay.to_gregorian(float(jdn))
        parts = solar_to_lunar(day, month, year, time_zone=float(timezone))
        return {
            "day": parts.day,
            "month": parts.month,
            "year": parts.year,
            "leap": parts.leap,
        }

    @staticmethod
    def get_new_moon_day(jdn, timezone):
        """Compatibility stub — use solar_to_lunar for full conversion."""
        del jdn, timezone
        return None

    @staticmethod
    def get_lunar_month11(new_moon, timezone):
        """Compatibility stub — use solar_to_lunar for full conversion."""
        del new_moon, timezone
        return None

    @staticmethod
    def get_leap_month_offset(month11, timezone):
        """Compatibility stub — use solar_to_lunar for full conversion."""
        del month11, timezone
        return None
