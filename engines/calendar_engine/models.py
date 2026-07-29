"""
BTE Platform
Calendar Engine Models

Định nghĩa toàn bộ Model dùng trong Calendar Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


# ==========================================================
# Location
# ==========================================================

@dataclass(slots=True)
class Location:
    """
    Thông tin vị trí địa lý.
    """

    latitude: float = 0.0
    longitude: float = 0.0
    elevation: float = 0.0
    timezone: float = 7.0
    country: str = "VN"
    province: str = ""
    city: str = ""


# ==========================================================
# Solar Date
# ==========================================================

@dataclass(slots=True)
class SolarDate:

    year: int
    month: int
    day: int

    hour: int = 0
    minute: int = 0
    second: int = 0

    timezone: float = 7.0


# ==========================================================
# Lunar Date
# ==========================================================

@dataclass(slots=True)
class LunarDate:

    year: int
    month: int
    day: int

    leap_month: bool = False

    hour: int = 0
    minute: int = 0
    second: int = 0


# ==========================================================
# Solar Term
# ==========================================================

@dataclass(slots=True)
class SolarTerm:

    index: int

    name: str

    longitude: float

    start: datetime | None = None

    end: datetime | None = None


# ==========================================================
# Ganzhi
# ==========================================================

@dataclass(slots=True)
class Ganzhi:

    heavenly_stem: str

    earthly_branch: str


# ==========================================================
# Four Pillars
# ==========================================================

@dataclass(slots=True)
class FourPillars:

    year: Ganzhi

    month: Ganzhi

    day: Ganzhi

    hour: Ganzhi


# ==========================================================
# Calendar Context
# ==========================================================

@dataclass(slots=True)
class CalendarContext:
    """
    Input của Calendar Engine.
    """

    datetime: datetime | None = None

    solar_date: SolarDate | None = None

    lunar_date: LunarDate | None = None

    location: Location | None = None

    timezone: float = 7.0

    operation: str = "full_calendar"

    options: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Calendar Result
# ==========================================================

@dataclass(slots=True)
class CalendarResult:
    """
    Output của Calendar Engine.
    """

    success: bool = True

    message: str = ""

    solar_date: SolarDate | None = None

    lunar_date: LunarDate | None = None

    solar_term: SolarTerm | None = None

    four_pillars: FourPillars | None = None

    julian_day: float | None = None

    sun_longitude: float | None = None

    moon_longitude: float | None = None

    moon_phase: str | None = None

    leap_month: bool = False

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Engine Config Model
# ==========================================================

@dataclass(slots=True)
class CalendarOptions:

    use_true_solar_time: bool = True

    use_delta_t: bool = True

    use_high_precision: bool = True

    cache_enabled: bool = True


# ==========================================================
# Engine State
# ==========================================================

@dataclass(slots=True)
class CalendarState:

    initialized: bool = False

    loaded: bool = False

    validated: bool = False

    calculated: bool = False
