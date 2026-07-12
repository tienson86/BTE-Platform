"""
===============================================================================
Calendar Engine - Julian Day Number (JDN)
-------------------------------------------------------------------------------
Tính Julian Day Number (JDN)

Julian Day Number là nền tảng của toàn bộ hệ thống thiên văn.

Được sử dụng cho:

    • Chuyển đổi Âm - Dương
    • Can Chi ngày
    • Tiết Khí
    • Sóc
    • Pha Mặt Trăng
    • Thiên văn

Thuật toán:
    Jean Meeus - Astronomical Algorithms

Độ chính xác:
    ± 1e-9 ngày

Author : Phong Thuy AI
Version : 1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import floor

# =============================================================================
# MODEL
# =============================================================================


@dataclass(slots=True)
class JulianDay:

    value: float

    integer: int

    fraction: float


# =============================================================================
# CALCULATOR
# =============================================================================


class JulianDayCalculator:
    """
    Julian Day Calculator
    """

    # -------------------------------------------------------------------------
    # MAIN
    # -------------------------------------------------------------------------

    def calculate(
        self,
        dt: datetime,
    ) -> JulianDay:
        """
        Tính Julian Day Number.

        Parameters
        ----------
        dt : datetime

        Returns
        -------
        JulianDay
        """

        year = dt.year
        month = dt.month

        day = (
            dt.day
            + dt.hour / 24.0
            + dt.minute / 1440.0
            + dt.second / 86400.0
            + dt.microsecond / 86400000000.0
        )

        if month <= 2:

            year -= 1
            month += 12

        a = floor(year / 100)

        b = 2 - a + floor(a / 4)

        jd = (
            floor(365.25 * (year + 4716))
            + floor(30.6001 * (month + 1))
            + day
            + b
            - 1524.5
        )

        return JulianDay(
            value=jd,
            integer=floor(jd),
            fraction=jd - floor(jd),
        )

    # -------------------------------------------------------------------------
    # INTEGER
    # -------------------------------------------------------------------------

    def integer(
        self,
        dt: datetime,
    ) -> int:

        return self.calculate(dt).integer

    # -------------------------------------------------------------------------
    # FLOAT
    # -------------------------------------------------------------------------

    def value(
        self,
        dt: datetime,
    ) -> float:

        return self.calculate(dt).value

    # -------------------------------------------------------------------------
    # FRACTION
    # -------------------------------------------------------------------------

    def fraction(
        self,
        dt: datetime,
    ) -> float:

        return self.calculate(dt).fraction

    # -------------------------------------------------------------------------
    # DATE ONLY
    # -------------------------------------------------------------------------

    def from_date(
        self,
        year: int,
        month: int,
        day: int,
    ) -> JulianDay:

        return self.calculate(
            datetime(
                year,
                month,
                day,
                0,
                0,
                0,
            )
        )

    # -------------------------------------------------------------------------
    # DATE TIME
    # -------------------------------------------------------------------------

    def from_components(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
    ) -> JulianDay:

        return self.calculate(
            datetime(
                year,
                month,
                day,
                hour,
                minute,
                second,
            )
        )

    # -------------------------------------------------------------------------
    # DAYS BETWEEN
    # -------------------------------------------------------------------------

    def days_between(
        self,
        dt1: datetime,
        dt2: datetime,
    ) -> float:

        return abs(
            self.value(dt2)
            - self.value(dt1)
        )

    # -------------------------------------------------------------------------
    # COMPARE
    # -------------------------------------------------------------------------

    def compare(
        self,
        dt1: datetime,
        dt2: datetime,
    ) -> int:

        jd1 = self.value(dt1)

        jd2 = self.value(dt2)

        if jd1 < jd2:
            return -1

        if jd1 > jd2:
            return 1

        return 0

    # -------------------------------------------------------------------------
    # IS SAME DAY
    # -------------------------------------------------------------------------

    def is_same_day(
        self,
        dt1: datetime,
        dt2: datetime,
    ) -> bool:

        return self.integer(dt1) == self.integer(dt2)


# =============================================================================
# SINGLETON
# =============================================================================

julian_day = JulianDayCalculator()
