"""
============================================================
BTE - Calendar Engine
------------------------------------------------------------
File        : julian.py
Module      : calendar_engine.core
Version     : 1.0.0
Author      : BTE Project
Encoding    : UTF-8
Python      : >=3.11
------------------------------------------------------------

MÔ TẢ

Module chuyển đổi giữa:

    Gregorian Date
            ⇅
    Julian Day Number (JDN)

Đây là module nền tảng của Calendar Engine.

Toàn bộ các module:

    solar.py
    moon.py
    jieqi.py
    ganzhi.py

đều sử dụng JDN do module này sinh ra.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass


# ==========================================================
# CONSTANTS
# ==========================================================

MIN_YEAR = 1583
MAX_YEAR = 9999


# ==========================================================
# DATA CLASS
# ==========================================================

@dataclass(slots=True)
class SolarDate:
    """
    Ngày Dương lịch.
    """

    year: int
    month: int
    day: int


# ==========================================================
# JULIAN ENGINE
# ==========================================================

class JulianEngine:
    """
    Engine xử lý Julian Day Number.
    """

    # ------------------------------------------------------

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """
        Kiểm tra năm nhuận Gregorian.
        """

        return (
            year % 400 == 0
            or (year % 4 == 0 and year % 100 != 0)
        )

    # ------------------------------------------------------

    @staticmethod
    def days_in_month(year: int, month: int) -> int:
        """
        Trả về số ngày trong tháng.
        """

        if month < 1 or month > 12:
            raise ValueError("Month must be 1..12")

        month_days = (
            31,
            28,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31,
        )

        if month == 2 and JulianEngine.is_leap_year(year):
            return 29

        return month_days[month - 1]

    # ------------------------------------------------------

    @staticmethod
    def validate_date(
        year: int,
        month: int,
        day: int,
    ) -> bool:
        """
        Kiểm tra ngày hợp lệ.
        """

        if year < MIN_YEAR:
            return False

        if year > MAX_YEAR:
            return False

        if month < 1 or month > 12:
            return False

        max_day = JulianEngine.days_in_month(year, month)

        return 1 <= day <= max_day

    # ------------------------------------------------------

    @staticmethod
    def solar_to_jdn(
        year: int,
        month: int,
        day: int,
    ) -> int:
        """
        Gregorian → Julian Day Number

        Thuật toán:
        Fliegel–Van Flandern
        """

        if not JulianEngine.validate_date(
            year,
            month,
            day,
        ):
            raise ValueError("Invalid Gregorian date")

        a = (14 - month) // 12

        y = year + 4800 - a

        m = month + 12 * a - 3

        jdn = (
            day
            + (153 * m + 2) // 5
            + 365 * y
            + y // 4
            - y // 100
            + y // 400
            - 32045
        )

        return jdn

    # ------------------------------------------------------

    @staticmethod
    def jdn_to_solar(jdn: int) -> SolarDate:
        """
        Julian Day Number → Gregorian
        """

        a = jdn + 32044

        b = (4 * a + 3) // 146097

        c = a - (146097 * b) // 4

        d = (4 * c + 3) // 1461

        e = c - (1461 * d) // 4

        m = (5 * e + 2) // 153

        day = e - (153 * m + 2) // 5 + 1

        month = m + 3 - 12 * (m // 10)

        year = (
            100 * b
            + d
            - 4800
            + (m // 10)
        )

        return SolarDate(
            year=year,
            month=month,
            day=day,
        )


# ==========================================================
# UNIT TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print("BTE JULIAN ENGINE TEST")

    print("=" * 60)

    jdn = JulianEngine.solar_to_jdn(
        2000,
        1,
        1,
    )

    print("2000-01-01 ->", jdn)

    solar = JulianEngine.jdn_to_solar(jdn)

    print(solar)

    print()

    print(
        JulianEngine.is_leap_year(2024)
    )

    print(
        JulianEngine.days_in_month(
            2024,
            2,
        )
    )

    print(
        JulianEngine.validate_date(
            2024,
            2,
            29,
        )
    )
