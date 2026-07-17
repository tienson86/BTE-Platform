"""
BTE Platform - Calendar Validator.

Kiểm tra dữ liệu đầu vào cho Calendar Engine.
"""

from __future__ import annotations

from datetime import datetime

from .exceptions import (
    CalendarValidationError,
    InvalidDateError,
    InvalidTimezoneError,
    InvalidCoordinateError,
)


class CalendarValidator:
    """
    Validator của Calendar Engine.
    """

    MIN_YEAR = 1
    MAX_YEAR = 9999

    MIN_LATITUDE = -90.0
    MAX_LATITUDE = 90.0

    MIN_LONGITUDE = -180.0
    MAX_LONGITUDE = 180.0

    MIN_TIMEZONE = -12
    MAX_TIMEZONE = 14

    # =====================================================
    # Context
    # =====================================================

    def validate_context(self, context) -> bool:
        """
        Kiểm tra CalendarContext.
        """

        if context is None:
            raise CalendarValidationError(
                "CalendarContext không được để trống."
            )

        if hasattr(context, "datetime") and context.datetime is not None:
            self.validate_datetime(context.datetime)

        if hasattr(context, "timezone"):
            self.validate_timezone(context.timezone)

        if hasattr(context, "latitude"):
            self.validate_latitude(context.latitude)

        if hasattr(context, "longitude"):
            self.validate_longitude(context.longitude)

        return True

    # =====================================================
    # DateTime
    # =====================================================

    def validate_datetime(
        self,
        value: datetime,
    ) -> bool:

        if not isinstance(value, datetime):
            raise InvalidDateError(
                "Giá trị phải là datetime."
            )

        if value.year < self.MIN_YEAR:
            raise InvalidDateError(
                f"Năm phải >= {self.MIN_YEAR}."
            )

        if value.year > self.MAX_YEAR:
            raise InvalidDateError(
                f"Năm phải <= {self.MAX_YEAR}."
            )

        return True

    # =====================================================
    # Solar Date
    # =====================================================

    def validate_solar_date(self, solar) -> bool:

        if solar is None:
            raise InvalidDateError(
                "SolarDate không được rỗng."
            )

        self.validate_year(solar.year)
        self.validate_month(solar.month)
        self.validate_day(solar.day)

        return True

    # =====================================================
    # Lunar Date
    # =====================================================

    def validate_lunar_date(self, lunar) -> bool:

        if lunar is None:
            raise InvalidDateError(
                "LunarDate không được rỗng."
            )

        self.validate_year(lunar.year)
        self.validate_month(lunar.month)
        self.validate_day(lunar.day)

        return True

    # =====================================================
    # Year
    # =====================================================

    def validate_year(
        self,
        year: int,
    ) -> bool:

        if not isinstance(year, int):
            raise InvalidDateError(
                "Năm phải là số nguyên."
            )

        if year < self.MIN_YEAR or year > self.MAX_YEAR:
            raise InvalidDateError(
                f"Năm phải nằm trong khoảng "
                f"{self.MIN_YEAR}-{self.MAX_YEAR}."
            )

        return True

    # =====================================================
    # Month
    # =====================================================

    def validate_month(
        self,
        month: int,
    ) -> bool:

        if not isinstance(month, int):
            raise InvalidDateError(
                "Tháng phải là số nguyên."
            )

        if month < 1 or month > 12:
            raise InvalidDateError(
                "Tháng phải từ 1 đến 12."
            )

        return True

    # =====================================================
    # Day
    # =====================================================

    def validate_day(
        self,
        day: int,
    ) -> bool:

        if not isinstance(day, int):
            raise InvalidDateError(
                "Ngày phải là số nguyên."
            )

        if day < 1 or day > 31:
            raise InvalidDateError(
                "Ngày phải từ 1 đến 31."
            )

        return True

    # =====================================================
    # Timezone
    # =====================================================

    def validate_timezone(
        self,
        timezone: int | float,
    ) -> bool:

        if not isinstance(timezone, (int, float)):
            raise InvalidTimezoneError(
                "Timezone phải là số."
            )

        if (
            timezone < self.MIN_TIMEZONE
            or timezone > self.MAX_TIMEZONE
        ):
            raise InvalidTimezoneError(
                f"Timezone phải nằm trong khoảng "
                f"{self.MIN_TIMEZONE} đến "
                f"{self.MAX_TIMEZONE}."
            )

        return True

    # =====================================================
    # Latitude
    # =====================================================

    def validate_latitude(
        self,
        latitude: float,
    ) -> bool:

        if latitude is None:
            return True

        if (
            latitude < self.MIN_LATITUDE
            or latitude > self.MAX_LATITUDE
        ):
            raise InvalidCoordinateError(
                "Latitude không hợp lệ."
            )

        return True

    # =====================================================
    # Longitude
    # =====================================================

    def validate_longitude(
        self,
        longitude: float,
    ) -> bool:

        if longitude is None:
            return True

        if (
            longitude < self.MIN_LONGITUDE
            or longitude > self.MAX_LONGITUDE
        ):
            raise InvalidCoordinateError(
                "Longitude không hợp lệ."
            )

        return True

    # =====================================================
    # Location
    # =====================================================

    def validate_location(
        self,
        latitude: float,
        longitude: float,
    ) -> bool:

        self.validate_latitude(latitude)
        self.validate_longitude(longitude)

        return True
