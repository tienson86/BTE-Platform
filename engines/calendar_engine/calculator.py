"""
BTE Platform - Calendar Calculator.

Điều phối các thuật toán lịch âm dương.
Không cài đặt trực tiếp công thức thiên văn.
"""

from __future__ import annotations

from datetime import datetime

from engines.core.base_calculator import BaseCalculator

from .loader import CalendarLoader

# Thuật toán hiện có
from .julian import JulianCalculator
from .moon.phase import MoonPhaseCalculator
from .moon.newmoon import NewMoonCalculator
from .solar.engine import SolarEngine


class CalendarCalculator(BaseCalculator):
    """
    Bộ điều phối tính toán của Calendar Engine.
    """

    def __init__(self):

        super().__init__()

        self.loader = CalendarLoader()

        self.julian = JulianCalculator()

        self.moon_phase = MoonPhaseCalculator()

        self.new_moon = NewMoonCalculator()

        self.solar = SolarEngine()

    # =====================================================
    # Julian
    # =====================================================

    def julian_day(
        self,
        dt: datetime,
    ):

        return self.julian.to_julian_day(dt)

    # =====================================================
    # Moon
    # =====================================================

    def moon_phase_at(
        self,
        dt: datetime,
    ):

        return self.moon_phase.phase(dt)

    def new_moon_before(
        self,
        dt: datetime,
    ):

        return self.new_moon.before(dt)

    def new_moon_after(
        self,
        dt: datetime,
    ):

        return self.new_moon.after(dt)

    # =====================================================
    # Solar
    # =====================================================

    def solar_longitude(
        self,
        dt: datetime,
    ):

        return self.solar.longitude(dt)

    def solar_term(
        self,
        dt: datetime,
    ):

        return self.solar.solar_term(dt)

    # =====================================================
    # Calendar
    # =====================================================

    def solar_to_lunar(
        self,
        dt: datetime,
        timezone: int = 7,
    ):

        return self.solar.solar_to_lunar(
            dt,
            timezone,
        )

    def lunar_to_solar(
        self,
        year: int,
        month: int,
        day: int,
        leap: bool = False,
        timezone: int = 7,
    ):

        return self.solar.lunar_to_solar(
            year,
            month,
            day,
            leap,
            timezone,
        )

    # =====================================================
    # Ganzhi
    # =====================================================

    def year_pillar(
        self,
        dt: datetime,
    ):

        return self.solar.year_pillar(dt)

    def month_pillar(
        self,
        dt: datetime,
    ):

        return self.solar.month_pillar(dt)

    def day_pillar(
        self,
        dt: datetime,
    ):

        return self.solar.day_pillar(dt)

    def hour_pillar(
        self,
        dt: datetime,
    ):

        return self.solar.hour_pillar(dt)
