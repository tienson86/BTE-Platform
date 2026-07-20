"""
BTE Platform

API Schemas

File: request.py
Version: 1.0
"""

from __future__ import annotations

from pydantic import Field

from .common import (
    AnalysisOptions,
    BaseRequest,
    BirthInfo,
)


# ==========================================================
# Calendar Request
# ==========================================================

class CalendarRequest(BaseRequest):
    """
    Request cho Calendar Engine.
    """

    birth: BirthInfo


# ==========================================================
# Bazi Request
# ==========================================================

class BaziRequest(BaseRequest):
    """
    Request cho Bazi Engine.
    """

    birth: BirthInfo


# ==========================================================
# Pattern Request
# ==========================================================

class PatternRequest(BaseRequest):
    """
    Request cho Pattern Engine.
    """

    birth: BirthInfo


# ==========================================================
# Score Request
# ==========================================================

class ScoreRequest(BaseRequest):
    """
    Request cho Score Engine.
    """

    birth: BirthInfo


# ==========================================================
# Interpretation Request
# ==========================================================

class InterpretationRequest(BaseRequest):
    """
    Request cho Interpretation Engine.
    """

    birth: BirthInfo

    options: AnalysisOptions = Field(
        default_factory=AnalysisOptions
    )


# ==========================================================
# Report Request
# ==========================================================

class ReportRequest(BaseRequest):
    """
    Request cho Report Engine.
    """

    birth: BirthInfo

    options: AnalysisOptions = Field(
        default_factory=AnalysisOptions
    )


# ==========================================================
# Full Analysis Request
# ==========================================================

class AnalysisRequest(BaseRequest):
    """
    Request chạy toàn bộ Engine Pipeline.
    """

    birth: BirthInfo

    options: AnalysisOptions = Field(
        default_factory=AnalysisOptions
    )
