"""
BTE Platform

Validation Utilities

File: validator.py
Version: 1.0
"""

from __future__ import annotations

from datetime import datetime


# ==========================================================
# Empty
# ==========================================================

def is_empty(value) -> bool:
    """
    Kiểm tra giá trị rỗng.
    """

    if value is None:
        return True

    if isinstance(value, str):
        return value.strip() == ""

    if isinstance(value, (list, tuple, dict, set)):
        return len(value) == 0

    return False


# ==========================================================
# Required
# ==========================================================

def require(value, field_name: str) -> None:
    """
    Kiểm tra bắt buộc.
    """

    if is_empty(value):

        raise ValueError(
            f"{field_name} is required."
        )


# ==========================================================
# Year
# ==========================================================

def validate_year(year: int) -> None:
    """
    Kiểm tra năm.
    """

    if year < 1900 or year > 2100:

        raise ValueError(
            "Year must be between 1900 and 2100."
        )


# ==========================================================
# Month
# ==========================================================

def validate_month(month: int) -> None:
    """
    Kiểm tra tháng.
    """

    if month < 1 or month > 12:

        raise ValueError(
            "Month must be between 1 and 12."
        )


# ==========================================================
# Day
# ==========================================================

def validate_day(
    year: int,
    month: int,
    day: int,
) -> None:
    """
    Kiểm tra ngày hợp lệ.
    """

    try:

        datetime(
            year,
            month,
            day,
        )

    except ValueError:

        raise ValueError(
            "Invalid date."
        )


# ==========================================================
# Hour
# ==========================================================

def validate_hour(hour: int) -> None:
    """
    Kiểm tra giờ.
    """

    if hour < 0 or hour > 23:

        raise ValueError(
            "Hour must be between 0 and 23."
        )


# ==========================================================
# Minute
# ==========================================================

def validate_minute(minute: int) -> None:
    """
    Kiểm tra phút.
    """

    if minute < 0 or minute > 59:

        raise ValueError(
            "Minute must be between 0 and 59."
        )


# ==========================================================
# Second
# ==========================================================

def validate_second(second: int) -> None:
    """
    Kiểm tra giây.
    """

    if second < 0 or second > 59:

        raise ValueError(
            "Second must be between 0 and 59."
        )


# ==========================================================
# Latitude
# ==========================================================

def validate_latitude(latitude: float) -> None:
    """
    Kiểm tra vĩ độ.
    """

    if latitude < -90 or latitude > 90:

        raise ValueError(
            "Latitude must be between -90 and 90."
        )


# ==========================================================
# Longitude
# ==========================================================

def validate_longitude(longitude: float) -> None:
    """
    Kiểm tra kinh độ.
    """

    if longitude < -180 or longitude > 180:

        raise ValueError(
            "Longitude must be between -180 and 180."
        )


# ==========================================================
# Timezone
# ==========================================================

def validate_timezone(
    timezone: float,
) -> None:
    """
    Kiểm tra múi giờ.
    """

    if timezone < -12 or timezone > 14:

        raise ValueError(
            "Timezone must be between -12 and +14."
        )


# ==========================================================
# Birth Data
# ==========================================================

def validate_birth_data(data: dict) -> None:
    """
    Kiểm tra dữ liệu ngày giờ sinh.
    """

    require(data.get("year"), "year")
    require(data.get("month"), "month")
    require(data.get("day"), "day")

    validate_year(data["year"])
    validate_month(data["month"])
    validate_day(
        data["year"],
        data["month"],
        data["day"],
    )

    if "hour" in data:
        validate_hour(data["hour"])

    if "minute" in data:
        validate_minute(data["minute"])

    if "second" in data:
        validate_second(data["second"])

    if "latitude" in data:
        validate_latitude(
            data["latitude"]
        )

    if "longitude" in data:
        validate_longitude(
            data["longitude"]
        )

    if "timezone" in data:
        validate_timezone(
            data["timezone"]
        )
