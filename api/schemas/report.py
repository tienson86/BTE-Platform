"""
BTE Platform

API Schemas

File: report.py
Version: 1.0
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from .common import ReportFormat


# ==========================================================
# Report Metadata
# ==========================================================

class ReportMetadataSchema(BaseModel):
    """
    Metadata của báo cáo.
    """

    title: str = ""

    subtitle: str = ""

    author: str = "BTE Platform"

    version: str = "1.0.0"

    language: str = "vi"

    created_at: str = ""


# ==========================================================
# Report Section
# ==========================================================

class ReportSectionSchema(BaseModel):
    """
    Một Section trong báo cáo.
    """

    id: str

    title: str

    content: str

    order: int = 0

    visible: bool = True

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


# ==========================================================
# Recommendation
# ==========================================================

class RecommendationSchema(BaseModel):
    """
    Khuyến nghị.
    """

    title: str

    content: str

    priority: int = 1


# ==========================================================
# Report Summary
# ==========================================================

class ReportSummarySchema(BaseModel):
    """
    Tổng quan báo cáo.
    """

    title: str = "Tổng quan"

    content: str = ""


# ==========================================================
# Report Schema
# ==========================================================

class ReportSchema(BaseModel):
    """
    Schema báo cáo.
    """

    metadata: ReportMetadataSchema = Field(
        default_factory=ReportMetadataSchema
    )

    summary: ReportSummarySchema = Field(
        default_factory=ReportSummarySchema
    )

    sections: list[ReportSectionSchema] = Field(
        default_factory=list
    )

    recommendations: list[
        RecommendationSchema
    ] = Field(
        default_factory=list
    )

    score: dict[str, Any] = Field(
        default_factory=dict
    )

    appendix: dict[str, Any] = Field(
        default_factory=dict
    )

    format: ReportFormat = (
        ReportFormat.MARKDOWN
    )
