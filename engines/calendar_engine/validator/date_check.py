"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    date_check.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Validate date and time.

=========================================================
"""

from datetime import datetime
import calendar


class DateCheck:
    """
    Kiểm tra tính hợp lệ của ngày và giờ.
    """

    MIN_YEAR = 1900
    MAX_YEAR = 2100


    def execute(self, context):

        input_data = context.get("input", {})

        solar_date = input_data.get("solar_date")

        solar_time = input_data.get("solar_time")

        self.validate_date(solar_date)

        self.validate_time(solar_time)

        self.validate_year(solar_date)

        context["date_checked"] = True

        return context


    # =====================================================

    # DATE

    # =====================================================

    def validate_date(self, value):

        try:

            datetime.strptime(
                value,
                "%d/%m/%Y"
            )

        except Exception:

            raise ValueError(
                f"Invalid date : {value}"
            )


    # =====================================================

    # TIME

    # =====================================================

    def validate_time(self, value):

        try:

            datetime.strptime(
                value,
                "%H:%M"
            )

        except Exception:

            raise ValueError(
                f"Invalid time : {value}"
            )


    # =====================================================

    # YEAR

    # =====================================================

    def validate_year(self, value):

        dt = datetime.strptime(
            value,
            "%d/%m/%Y"
        )

        year = dt.year

        if year < self.MIN_YEAR:

            raise ValueError(
                f"Year must be >= {self.MIN_YEAR}"
            )

        if year > self.MAX_YEAR:

            raise ValueError(
                f"Year must be <= {self.MAX_YEAR}"
            )


    # =====================================================

    # LEAP YEAR

    # =====================================================

    def is_leap_year(self, year):

        return calendar.isleap(year)


    # =====================================================

    # DAYS IN MONTH

    # =====================================================

    def days_in_month(self, month, year):

        return calendar.monthrange(
            year,
            month
        )[1]
