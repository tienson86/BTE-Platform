"""
BTE Platform
Report Engine

File: report.py
Version: 1.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


# ==========================================================
# Report Format
# ==========================================================

class ReportFormat(str, Enum):
    """Các định dạng xuất báo cáo."""

    TEXT = "text"
    MARKDOWN = "markdown"
    HTML = "html"
    JSON = "json"
    PDF = "pdf"
    DOCX = "docx"


# ==========================================================
# Report Status
# ==========================================================

class ReportStatus(str, Enum):
    """Trạng thái báo cáo."""

    DRAFT = "draft"
    COMPLETED = "completed"
    EXPORTED = "exported"


# ==========================================================
# Metadata
# ==========================================================

@dataclass(slots=True)
class ReportMetadata:
    """Thông tin metadata của báo cáo."""

    title: str = ""

    author: str = "BTE Platform"

    version: str = "1.0"

    language: str = "vi"

    created_at: datetime = field(default_factory=datetime.utcnow)

    generated_at: datetime | None = None


# ==========================================================
# Summary
# ==========================================================

@dataclass(slots=True)
class ReportSummary:
    """Tổng quan báo cáo."""

    title: str = ""

    content: str = ""


# ==========================================================
# Recommendation
# ==========================================================

@dataclass(slots=True)
class ReportRecommendation:
    """Khuyến nghị."""

    title: str

    content: str

    priority: int = 1


# ==========================================================
# Report
# ==========================================================

@dataclass(slots=True)
class Report:
    """
    Model báo cáo hoàn chỉnh.
    """

    metadata: ReportMetadata = field(
        default_factory=ReportMetadata
    )

    summary: ReportSummary = field(
        default_factory=ReportSummary
    )

    sections: list[Any] = field(
        default_factory=list
    )

    recommendations: list[ReportRecommendation] = field(
        default_factory=list
    )

    score: dict[str, Any] = field(
        default_factory=dict
    )

    appendix: dict[str, Any] = field(
        default_factory=dict
    )

    status: ReportStatus = ReportStatus.DRAFT

    format: ReportFormat = ReportFormat.MARKDOWN
