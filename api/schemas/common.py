"""
BTE Platform

API Schemas

File: common.py
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


class ReportFormat(str, Enum):
    """
    Định dạng báo cáo.
    """

    TEXT = "text"

    MARKDOWN = "markdown"

    HTML = "html"

    JSON = "json"


# ==========================================================
# Base Models
# ==========================================================

class Location(BaseModel):
    """
    Thông tin địa điểm.
    """

    latitude: float | None = None

    longitude: float | None = None

    timezone: str = "Asia/Ho_Chi_Minh"

    place: str | None = None


class BirthInfo(BaseModel):
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

    location: Location = Field(
        default_factory=Location
    )


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

    report_format: ReportFormat = ReportFormat.MARKDOWN

    language: Language = Language.VI


class BaseRequest(BaseModel):
    """
    Request cơ sở.
    """

    request_id: str | None = None

    client: str | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class BaseResponse(BaseModel):
    """
    Response cơ sở.
    """

    success: bool = True

    message: str = ""

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )
