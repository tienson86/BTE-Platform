"""
===============================================================================
Bazi Engine - Validator
-------------------------------------------------------------------------------
Kiểm tra dữ liệu đầu vào trước khi tính toán.

Không chứa thuật toán Bát Tự.
===============================================================================
"""

from __future__ import annotations

from datetime import datetime

from .constants import GENDERS


class Validator:
    """
    Bộ kiểm tra dữ liệu đầu vào.
    """

    # -------------------------------------------------------------------------
    # YEAR
    # -------------------------------------------------------------------------

    @staticmethod
    def validate_year(year: int) -> None:

        if year < 1600 or year > 2300:
            raise ValueError("Năm ngoài phạm vi hỗ trợ.")

    # -------------------------------------------------------------------------
    # MONTH
    # -------------------------------------------------------------------------

    @staticmethod
    def validate_month(month: int) -> None:

        if month < 1 or month > 12:
            raise ValueError("Tháng không hợp lệ.")

    # -------------------------------------------------------------------------
    # DAY
    # -------------------------------------------------------------------------

    @staticmethod
    def validate_day(day: int) -> None:

        if day < 1 or day > 31:
            raise ValueError("Ngày không hợp lệ.")

    # -------------------------------------------------------------------------
    # HOUR
    # -------------------------------------------------------------------------

    @staticmethod
    def validate_hour(hour: int) -> None:

        if hour < 0 or hour > 23:
            raise ValueError("Giờ không hợp lệ.")

    # -------------------------------------------------------------------------
    # MINUTE
    # -------------------------------------------------------------------------

    @staticmethod
    def validate_minute(minute: int) -> None:

        if minute < 0 or minute > 59:
            raise ValueError("Phút không hợp lệ.")

    # -------------------------------------------------------------------------
    # GENDER
    # -------------------------------------------------------------------------

    @staticmethod
    def validate_gender(gender: str) -> None:

        if gender not in GENDERS:
            raise ValueError("Giới tính không hợp lệ.")

    # -------------------------------------------------------------------------
    # DATETIME
    # -------------------------------------------------------------------------

    @staticmethod
    def validate_datetime(
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
    ) -> None:

        datetime(year, month, day, hour, minute)

    # -------------------------------------------------------------------------
    # FULL INPUT
    # -------------------------------------------------------------------------

    @classmethod
    def validate_input(
        cls,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        gender: str,
    ) -> None:

        cls.validate_year(year)
        cls.validate_month(month)
        cls.validate_day(day)
        cls.validate_hour(hour)
        cls.validate_minute(minute)
        cls.validate_gender(gender)
        cls.validate_datetime(
            year,
            month,
            day,
            hour,
            minute,
        )


# =============================================================================
# Singleton
# =============================================================================

validator = Validator()
