"""
BTE Platform

API Schemas

File: request.py
Version: 1.0
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# ==========================================================
# Enum
# ==========================================================

class Gender(str, Enum):
    """
    Giới tính.
    """

    MALE = "male"

    FEMALE = "female"


class CalendarType(str, Enum):
    """
    Loại lịch.
    """

    SOLAR = "solar"

    LUNAR = "lunar"


class Language(str, Enum):
    """
    Ngôn ngữ.
    """

    VI = "vi"

    EN = "en"


# ==========================================================
# Location
# ==========================================================

class LocationRequest(BaseModel):
    """
    Thông tin vị trí.
    """

    latitude: float | None = None

    longitude: float | None = None

    timezone: str = "Asia/Ho_Chi_Minh"

    place: str | None = None


# ==========================================================
# Birth
# ==========================================================

class BirthRequest(BaseModel):
    """
    Thông tin ngày giờ sinh.
    """

    date: str = Field(
        ...,
        description="YYYY-MM-DD",
    )

    time: str = Field(
        ...,
        description="HH:MM",
    )

    gender: Gender

    calendar: CalendarType = CalendarType.SOLAR

    location: LocationRequest = Field(
        default_factory=LocationRequest
    )


# ==========================================================
# Analysis Options
# ==========================================================

class AnalysisOptions(BaseModel):
    """
    Tùy chọn phân tích.
    """

    calculate_calendar: bool = True

    calculate_bazi: bool = True

    calculate_pattern: bool = True

    calculate_score: bool = True

    calculate_interpretation: bool = True

    generate_report: bool = True

    report_format: str = "markdown"

    language: Language = Language.VI


# ==========================================================
# Base Request
# ==========================================================

class BaseRequest(BaseModel):
    """
    Request cơ sở.
    """

    request_id: str | None = None

    client: str | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


# ==========================================================
# Calendar
# ==========================================================

class CalendarRequest(BaseRequest):

    birth: BirthRequest


# ==========================================================
# Bazi
# ==========================================================

class BaziRequest(BaseRequest):

    birth: BirthRequest


# ==========================================================
# Score
# ==========================================================

class ScoreRequest(BaseRequest):

    birth: BirthRequest


# ==========================================================
# Interpretation
# ==========================================================

class InterpretationRequest(BaseRequest):

    birth: BirthRequest

    options: AnalysisOptions = Field(
        default_factory=AnalysisOptions
    )


# ==========================================================
# Report
# ==========================================================

class ReportRequest(BaseRequest):

    birth: BirthRequest

    options: AnalysisOptions = Field(
        default_factory=AnalysisOptions
    )


# ==========================================================
# Full Pipeline
# ==========================================================

class AnalysisRequest(BaseRequest):
    """
    Chạy toàn bộ Engine Pipeline.
    """

    birth: BirthRequest

    options: AnalysisOptions = Field(
        default_factory=AnalysisOptions
    )
