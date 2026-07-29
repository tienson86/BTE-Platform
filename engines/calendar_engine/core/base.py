"""
============================================================
BTE - Calendar Engine
------------------------------------------------------------
File        : base.py
Module      : calendar_engine.core
Version     : 1.0.0
Author      : BTE Project
Encoding    : UTF-8
Python      : >=3.11
------------------------------------------------------------

Module nền tảng dùng chung cho toàn bộ Calendar Engine.

Các module sử dụng:

    julian.py
    solar.py
    moon.py
    jieqi.py
    ganzhi.py
    converter.py

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import pi

# ==========================================================
# ENGINE VERSION
# ==========================================================

ENGINE_NAME = "BTE Calendar Engine"

ENGINE_VERSION = "1.0.0"

# ==========================================================
# TIMEZONE
# ==========================================================

DEFAULT_TIMEZONE = 7

UTC_TIMEZONE = 0

# ==========================================================
# MATHEMATICAL CONSTANTS
# ==========================================================

PI = pi

RAD = PI / 180.0

DEG = 180.0 / PI

# ==========================================================
# ASTRONOMICAL CONSTANTS
# ==========================================================

J2000 = 2451545.0

SYNODIC_MONTH = 29.530588853

TROPICAL_YEAR = 365.242189

EARTH_OBLIQUITY = 23.439291111

# ==========================================================
# YEAR RANGE
# ==========================================================

MIN_YEAR = 1583

MAX_YEAR = 9999

# ==========================================================
# DATACLASS
# ==========================================================

@dataclass(slots=True)
class SolarDate:

    year: int

    month: int

    day: int


@dataclass(slots=True)
class SolarTime:

    hour: int

    minute: int

    second: int = 0


@dataclass(slots=True)
class SolarDateTime:

    year: int

    month: int

    day: int

    hour: int

    minute: int

    second: int = 0

    timezone: int = DEFAULT_TIMEZONE


@dataclass(slots=True)
class LunarDate:

    year: int

    month: int

    day: int

    leap: bool = False


@dataclass(slots=True)
class JulianDate:

    jdn: float


# ==========================================================
# BASE EXCEPTION
# ==========================================================

class CalendarEngineError(Exception):
    """
    Base Exception
    """


class InvalidDateError(CalendarEngineError):
    """
    Sai ngày tháng năm
    """


class InvalidTimeError(CalendarEngineError):
    """
    Sai giờ phút
    """


class InvalidTimezoneError(CalendarEngineError):
    """
    Sai múi giờ
    """


class CalculationError(CalendarEngineError):
    """
    Lỗi tính toán
    """


# ==========================================================
# COMMON FUNCTIONS
# ==========================================================

def deg_to_rad(value: float) -> float:
    """
    Degree -> Radian
    """

    return value * RAD


def rad_to_deg(value: float) -> float:
    """
    Radian -> Degree
    """

    return value * DEG


def normalize_degree(value: float) -> float:
    """
    Chuẩn hóa góc về 0~360
    """

    return value % 360.0


def normalize_hour(value: float) -> float:
    """
    Chuẩn hóa giờ
    """

    return value % 24.0


def utc_now() -> datetime:
    """
    UTC hiện tại
    """

    return datetime.utcnow()


# ==========================================================
# VALIDATION
# ==========================================================

def validate_timezone(timezone: int) -> bool:

    return -12 <= timezone <= 14


def validate_hour(hour: int) -> bool:

    return 0 <= hour <= 23


def validate_minute(minute: int) -> bool:

    return 0 <= minute <= 59


def validate_second(second: int) -> bool:

    return 0 <= second <= 59


# ==========================================================
# EXPORT
# ==========================================================

__all__ = [

    "ENGINE_NAME",
    "ENGINE_VERSION",

    "PI",
    "RAD",
    "DEG",

    "J2000",
    "SYNODIC_MONTH",
    "TROPICAL_YEAR",
    "EARTH_OBLIQUITY",

    "MIN_YEAR",
    "MAX_YEAR",

    "DEFAULT_TIMEZONE",
    "UTC_TIMEZONE",

    "SolarDate",
    "SolarTime",
    "SolarDateTime",
    "LunarDate",
    "JulianDate",

    "CalendarEngineError",
    "InvalidDateError",
    "InvalidTimeError",
    "InvalidTimezoneError",
    "CalculationError",

    "deg_to_rad",
    "rad_to_deg",
    "normalize_degree",
    "normalize_hour",
    "utc_now",

    "validate_timezone",
    "validate_hour",
    "validate_minute",
    "validate_second",
]

# ==========================================================
# UNIT TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print(ENGINE_NAME)

    print("Version :", ENGINE_VERSION)

    print("=" * 60)

    print("PI =", PI)

    print("RAD =", RAD)

    print("DEG =", DEG)

    print()

    print("J2000 =", J2000)

    print("Synodic Month =", SYNODIC_MONTH)

    print("Tropical Year =", TROPICAL_YEAR)

    print()

    print("Normalize 725° =", normalize_degree(725))

    print("90° -> Rad =", deg_to_rad(90))

    print("π -> Deg =", rad_to_deg(PI))

    print()

    print("UTC =", utc_now())
