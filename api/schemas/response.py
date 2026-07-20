"""
BTE Platform

API Schemas

File: response.py
Version: 1.0
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from .common import BaseResponse


# ==========================================================
# Error Response
# ==========================================================

class ErrorResponse(BaseResponse):
    """
    Response khi xảy ra lỗi.
    """

    success: bool = False

    error_code: str = ""

    details: list[str] = Field(
        default_factory=list
    )


# ==========================================================
# Calendar Response
# ==========================================================

class CalendarResponse(BaseResponse):
    """
    Response của Calendar Engine.
    """

    data: dict[str, Any] = Field(
        default_factory=dict
    )


# ==========================================================
# Bazi Response
# ==========================================================

class BaziResponse(BaseResponse):
    """
    Response của Bazi Engine.
    """

    data: dict[str, Any] = Field(
        default_factory=dict
    )


# ==========================================================
# Pattern Response
# ==========================================================

class PatternResponse(BaseResponse):
    """
    Response của Pattern Engine.
    """

    data: dict[str, Any] = Field(
        default_factory=dict
    )


# ==========================================================
# Score Response
# ==========================================================

class ScoreResponse(BaseResponse):
    """
    Response của Score Engine.
    """

    data: dict[str, Any] = Field(
        default_factory=dict
    )


# ==========================================================
# Interpretation Response
# ==========================================================

class InterpretationResponse(BaseResponse):
    """
    Response của Interpretation Engine.
    """

    data: dict[str, Any] = Field(
        default_factory=dict
    )


# ==========================================================
# Report Response
# ==========================================================

class ReportResponse(BaseResponse):
    """
    Response của Report Engine.
    """

    data: dict[str, Any] = Field(
        default_factory=dict
    )


# ==========================================================
# Analysis Response
# ==========================================================

class AnalysisResponse(BaseResponse):
    """
    Response chạy toàn bộ Pipeline.
    """

    data: dict[str, Any] = Field(
        default_factory=dict
    )


# ==========================================================
# Health Response
# ==========================================================

class HealthResponse(BaseResponse):
    """
    Response kiểm tra trạng thái hệ thống.
    """

    service: str = "BTE Platform"

    version: str = "1.0.0"

    status: str = "healthy"
