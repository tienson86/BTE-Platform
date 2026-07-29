"""
BTE Platform - Calendar Service.

Lớp Service là API công khai của Calendar Engine.
Các Engine khác chỉ tương tác với CalendarService,
không gọi trực tiếp CalendarCalculator.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from .engine import CalendarEngine
from .models import (
    CalendarContext,
    CalendarResult,
    SolarDate,
    LunarDate,
    SolarTerm,
)
from .validator import CalendarValidator


class CalendarService:
    """
    Public Service của Calendar Engine.
    """

    def __init__(
        self,
        engine: Optional[CalendarEngine] = None,
    ) -> None:

        self._engine = engine or CalendarEngine()
        self._validator = CalendarValidator()

    # =====================================================
    # API chính
    # =====================================================

    def execute(
        self,
        context: CalendarContext,
    ) -> CalendarResult:
        """
        Thực thi Calendar Engine.
        """

        self._validator.validate_context(context)

        return self._engine.execute(context)

    # =====================================================
    # API chuyển đổi lịch
    # =====================================================

    def solar_to_lunar(
        self,
        solar: SolarDate,
    ) -> LunarDate:

        self._validator.validate_solar_date(solar)

        context = CalendarContext(
            solar_date=solar,
            operation="solar_to_lunar",
        )

        result = self.execute(context)

        return result.lunar_date

    def lunar_to_solar(
        self,
        lunar: LunarDate,
    ) -> SolarDate:

        self._validator.validate_lunar_date(lunar)

        context = CalendarContext(
            lunar_date=lunar,
            operation="lunar_to_solar",
        )

        result = self.execute(context)

        return result.solar_date

    # =====================================================
    # API Tiết khí
    # =====================================================

    def get_solar_term(
        self,
        date: datetime,
    ) -> SolarTerm:

        self._validator.validate_datetime(date)

        context = CalendarContext(
            datetime=date,
            operation="solar_term",
        )

        result = self.execute(context)

        return result.solar_term

    # =====================================================
    # API Can Chi
    # =====================================================

    def get_year_pillar(
        self,
        date: datetime,
    ):

        context = CalendarContext(
            datetime=date,
            operation="year_pillar",
        )

        return self.execute(context).year_pillar

    def get_month_pillar(
        self,
        date: datetime,
    ):

        context = CalendarContext(
            datetime=date,
            operation="month_pillar",
        )

        return self.execute(context).month_pillar

    def get_day_pillar(
        self,
        date: datetime,
    ):

        context = CalendarContext(
            datetime=date,
            operation="day_pillar",
        )

        return self.execute(context).day_pillar

    def get_hour_pillar(
        self,
        date: datetime,
    ):

        context = CalendarContext(
            datetime=date,
            operation="hour_pillar",
        )

        return self.execute(context).hour_pillar

    # =====================================================
    # API Bát tự
    # =====================================================

    def build_calendar(
        self,
        date: datetime,
        timezone: int = 7,
    ) -> CalendarResult:
        """
        Sinh toàn bộ dữ liệu lịch phục vụ Bazi Engine.
        """

        context = CalendarContext(
            datetime=date,
            timezone=timezone,
            operation="full_calendar",
        )

        return self.execute(context)

    # =====================================================
    # Kiểm tra
    # =====================================================

    def validate(
        self,
        context: CalendarContext,
    ) -> bool:

        return self._validator.validate_context(context)

    # =====================================================
    # Thông tin Engine
    # =====================================================

    @property
    def engine(self) -> CalendarEngine:

        return self._engine
