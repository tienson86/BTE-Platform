"""
===============================================================================
Calendar Engine
-------------------------------------------------------------------------------
Module trung tâm của Calendar Engine.

Chức năng

    • Chuyển đổi Dương lịch ⇄ Âm lịch
    • Julian Day Number
    • Tiết Khí
    • Pha Mặt Trăng
    • Sóc (New Moon)
    • Thiên văn cơ bản

Đây là API duy nhất mà Bazi Engine sử dụng.

Tác giả : Phong Thuy AI
Phiên bản : 1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# =============================================================================
# Calendar Modules
# =============================================================================

from .moon.phase import MoonPhaseCalculator
from .moon.newmoon import NewMoonCalculator

# Nếu đã xây dựng thì bỏ comment
#
# from .solar_terms.engine import SolarTermCalculator
# from .lunar.engine import LunarCalendarCalculator
# from .julian.engine import JulianDayCalculator

# =============================================================================
# Result Models
# =============================================================================


@dataclass(slots=True)
class CalendarContext:
    """
    Toàn bộ dữ liệu lịch sau khi tính toán.
    """

    # -----------------------------------------------------------------
    # Input
    # -----------------------------------------------------------------

    birth_datetime: datetime

    timezone: str

    # -----------------------------------------------------------------
    # Solar Calendar
    # -----------------------------------------------------------------

    solar_year: int

    solar_month: int

    solar_day: int

    solar_hour: int

    solar_minute: int

    # -----------------------------------------------------------------
    # Lunar Calendar
    # -----------------------------------------------------------------

    lunar_year: Optional[int] = None

    lunar_month: Optional[int] = None

    lunar_day: Optional[int] = None

    leap_month: bool = False

    # -----------------------------------------------------------------
    # Julian
    # -----------------------------------------------------------------

    julian_day: Optional[float] = None

    # -----------------------------------------------------------------
    # Solar Term
    # -----------------------------------------------------------------

    solar_term: Optional[str] = None

    solar_term_index: Optional[int] = None

    solar_longitude: Optional[float] = None

    month_branch: Optional[str] = None

    li_chun_datetime: Optional[datetime] = None

    # -----------------------------------------------------------------
    # Moon
    # -----------------------------------------------------------------

    moon_phase: Optional[str] = None

    moon_age: Optional[float] = None

    next_new_moon: Optional[datetime] = None

    previous_new_moon: Optional[datetime] = None

    # -----------------------------------------------------------------
    # Extra
    # -----------------------------------------------------------------

    weekday: Optional[int] = None

    day_of_year: Optional[int] = None


# =============================================================================
# Engine
# =============================================================================


class CalendarEngine:
    """
    Calendar Engine Orchestrator.
    """

    def __init__(self):

        self.phase = MoonPhaseCalculator()

        self.newmoon = NewMoonCalculator()

        # self.solar_term = SolarTermCalculator()

        # self.lunar = LunarCalendarCalculator()

        # self.julian = JulianDayCalculator()

    # -------------------------------------------------------------------------
    # Main
    # -------------------------------------------------------------------------

    def calculate(
        self,
        birth_datetime: datetime,
        timezone: str = "Asia/Ho_Chi_Minh",
    ) -> CalendarContext:

        """
        Tính toàn bộ dữ liệu lịch.
        """

        context = CalendarContext(

            birth_datetime=birth_datetime,

            timezone=timezone,

            solar_year=birth_datetime.year,

            solar_month=birth_datetime.month,

            solar_day=birth_datetime.day,

            solar_hour=birth_datetime.hour,

            solar_minute=birth_datetime.minute,

        )

        # =============================================================
        # Weekday
        # =============================================================

        context.weekday = birth_datetime.weekday()

        context.day_of_year = birth_datetime.timetuple().tm_yday

        # =============================================================
        # Lunar
        # =============================================================

        # lunar = self.lunar.calculate(birth_datetime)
        #
        # context.lunar_year = lunar.year
        # context.lunar_month = lunar.month
        # context.lunar_day = lunar.day
        # context.leap_month = lunar.leap

        # =============================================================
        # Julian Day
        # =============================================================

        # context.julian_day = self.julian.calculate(birth_datetime)

        # =============================================================
        # Solar Term
        # =============================================================

        # solar = self.solar_term.calculate(birth_datetime)
        #
        # context.solar_term = solar.name
        # context.solar_term_index = solar.index
        # context.solar_longitude = solar.longitude
        # context.month_branch = solar.month_branch
        # context.li_chun_datetime = solar.li_chun

        # =============================================================
        # Moon Phase
        # =============================================================

        try:

            phase = self.phase.calculate(birth_datetime)

            context.moon_phase = phase.phase

            context.moon_age = phase.age

        except Exception:

            pass

        # =============================================================
        # New Moon
        # =============================================================

        try:

            newmoon = self.newmoon.calculate(birth_datetime)

            context.previous_new_moon = newmoon.previous

            context.next_new_moon = newmoon.next

        except Exception:

            pass

        return context

    # -------------------------------------------------------------------------
    # Convenience Methods
    # -------------------------------------------------------------------------

    def get_solar_term(self, birth_datetime: datetime):

        """
        Trả về Tiết Khí.
        """

        return self.calculate(birth_datetime).solar_term

    def get_month_branch(self, birth_datetime: datetime):

        """
        Trả về Địa Chi tháng.
        """

        return self.calculate(birth_datetime).month_branch

    def get_li_chun(self, birth_datetime: datetime):

        """
        Trả về thời điểm Lập Xuân.
        """

        return self.calculate(birth_datetime).li_chun_datetime

    def get_julian_day(self, birth_datetime: datetime):

        """
        Trả về Julian Day.
        """

        return self.calculate(birth_datetime).julian_day

    def get_lunar(self, birth_datetime: datetime):

        """
        Trả về dữ liệu âm lịch.
        """

        ctx = self.calculate(birth_datetime)

        return (
            ctx.lunar_year,
            ctx.lunar_month,
            ctx.lunar_day,
        )


# =============================================================================
# Singleton
# =============================================================================

calendar_engine = CalendarEngine()
