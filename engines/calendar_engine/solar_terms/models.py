"""
===============================================================================
Calendar Engine - Solar Terms Models
-------------------------------------------------------------------------------
Định nghĩa các Model dùng cho module Tiết Khí.

Nguyên tắc:
- Chỉ chứa dataclass.
- Không chứa thuật toán.
- Không chứa logic tính toán.

Các model này được sử dụng bởi:
    • calculator.py
    • engine.py
    • month_pillar.py
    • CalendarEngine
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


# =============================================================================
# SOLAR LONGITUDE
# =============================================================================

@dataclass(slots=True)
class SolarLongitude:
    """
    Kinh độ biểu kiến của Mặt Trời.
    """

    value: float          # Độ (0° - 360°)

    radians: float

    julian_day: float


# =============================================================================
# SOLAR TERM
# =============================================================================

@dataclass(slots=True)
class SolarTerm:
    """
    Một Tiết Khí.
    """

    index: int

    name: str

    longitude: float

    month_branch: str

    start: Optional[datetime] = None

    end: Optional[datetime] = None


# =============================================================================
# SOLAR TERM RESULT
# =============================================================================

@dataclass(slots=True)
class SolarTermResult:
    """
    Kết quả xác định Tiết Khí.
    """

    birth_datetime: datetime

    solar_longitude: SolarLongitude

    current: SolarTerm

    previous: Optional[SolarTerm]

    next: Optional[SolarTerm]


# =============================================================================
# LẬP XUÂN
# =============================================================================

@dataclass(slots=True)
class LiChunResult:
    """
    Thời điểm Lập Xuân của năm.
    """

    year: int

    datetime: datetime


# =============================================================================
# MONTH BRANCH
# =============================================================================

@dataclass(slots=True)
class MonthBranchResult:
    """
    Địa Chi tháng theo Tiết Khí.
    """

    branch: str

    index: int

    solar_term: str


# =============================================================================
# CONTEXT
# =============================================================================

@dataclass(slots=True)
class SolarTermContext:
    """
    Context hoàn chỉnh của module Solar Terms.
    """

    result: SolarTermResult

    li_chun: LiChunResult

    month_branch: MonthBranchResult
