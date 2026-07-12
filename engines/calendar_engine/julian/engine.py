"""
===============================================================================
Calendar Engine - Julian Engine
-------------------------------------------------------------------------------
Module trung tâm của Julian Engine.

Chức năng
---------
- Cung cấp API thống nhất cho toàn bộ Julian Day Number.
- Bao bọc (Facade) JulianDayCalculator.
- Trả về các kết quả chuẩn cho Calendar Engine.

Module sử dụng:
    • Bazi Engine
    • Calendar Engine
    • Solar Terms
    • Lunar Converter
    • Moon Phase
    • New Moon

Author : Phong Thuy AI
Version : 1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .jdn import JulianDay
from .jdn import JulianDayCalculator


# =============================================================================
# RESULT MODEL
# =============================================================================

@dataclass(slots=True)
class JulianContext:
    """
    Kết quả chuẩn của Julian Engine.
    """

    datetime: datetime

    julian_day: float

    julian_integer: int

    julian_fraction: float


# =============================================================================
# ENGINE
# =============================================================================

class JulianEngine:
    """
    Julian Engine.

    Đây là API chính cho toàn bộ hệ thống.
    """

    def __init__(self):

        self.calculator = JulianDayCalculator()

    # -------------------------------------------------------------------------
    # MAIN
    # -------------------------------------------------------------------------

    def calculate(
        self,
        dt: datetime,
    ) -> JulianContext:
        """
        Tính toàn bộ dữ liệu Julian.
        """

        jd: JulianDay = self.calculator.calculate(dt)

        return JulianContext(
            datetime=dt,
            julian_day=jd.value,
            julian_integer=jd.integer,
            julian_fraction=jd.fraction,
        )

    # -------------------------------------------------------------------------
    # VALUE
    # -------------------------------------------------------------------------

    def value(
        self,
        dt: datetime,
    ) -> float:
        """
        Trả về Julian Day Number.
        """

        return self.calculator.value(dt)

    # -------------------------------------------------------------------------
    # INTEGER
    # -------------------------------------------------------------------------

    def integer(
        self,
        dt: datetime,
    ) -> int:
        """
        Trả về phần nguyên của JDN.
        """

        return self.calculator.integer(dt)

    # -------------------------------------------------------------------------
    # FRACTION
    # -------------------------------------------------------------------------

    def fraction(
        self,
        dt: datetime,
    ) -> float:
        """
        Trả về phần thập phân của JDN.
        """

        return self.calculator.fraction(dt)

    # -------------------------------------------------------------------------
    # FROM DATE
    # -------------------------------------------------------------------------

    def from_date(
        self,
        year: int,
        month: int,
        day: int,
    ) -> JulianContext:
        """
        Tính JDN từ ngày.
        """

        dt = datetime(year, month, day)

        return self.calculate(dt)

    # -------------------------------------------------------------------------
    # FROM COMPONENTS
    # -------------------------------------------------------------------------

    def from_components(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
    ) -> JulianContext:
        """
        Tính JDN từ các thành phần ngày giờ.
        """

        dt = datetime(
            year,
            month,
            day,
            hour,
            minute,
            second,
        )

        return self.calculate(dt)

    # -------------------------------------------------------------------------
    # DAYS BETWEEN
    # -------------------------------------------------------------------------

    def days_between(
        self,
        dt1: datetime,
        dt2: datetime,
    ) -> float:
        """
        Khoảng cách giữa hai thời điểm (ngày).
        """

        return self.calculator.days_between(dt1, dt2)

    # -------------------------------------------------------------------------
    # COMPARE
    # -------------------------------------------------------------------------

    def compare(
        self,
        dt1: datetime,
        dt2: datetime,
    ) -> int:
        """
        So sánh hai thời điểm.

        Returns
        -------
        -1 : dt1 < dt2
         0 : dt1 = dt2
         1 : dt1 > dt2
        """

        return self.calculator.compare(dt1, dt2)

    # -------------------------------------------------------------------------
    # SAME DAY
    # -------------------------------------------------------------------------

    def is_same_day(
        self,
        dt1: datetime,
        dt2: datetime,
    ) -> bool:
        """
        Hai thời điểm có cùng JDN hay không.
        """

        return self.calculator.is_same_day(dt1, dt2)


# =============================================================================
# SINGLETON
# =============================================================================

julian_engine = JulianEngine()
