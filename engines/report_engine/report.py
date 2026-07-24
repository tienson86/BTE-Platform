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
    WP6 ReportModel — báo cáo hoàn chỉnh + artifacts + template coverage.
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

    html: str = ""
    markdown: str = ""
    pdf_path: str = ""
    templates_used: list[dict[str, Any]] = field(default_factory=list)
    templates_unused: list[dict[str, Any]] = field(default_factory=list)
    template_coverage: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize report for JSON export / pipeline."""
        return {
            "metadata": {
                "title": self.metadata.title,
                "author": self.metadata.author,
                "version": self.metadata.version,
                "language": self.metadata.language,
                "created_at": (
                    self.metadata.created_at.isoformat()
                    if self.metadata.created_at
                    else None
                ),
                "generated_at": (
                    self.metadata.generated_at.isoformat()
                    if self.metadata.generated_at
                    else None
                ),
            },
            "summary": {
                "title": self.summary.title,
                "content": self.summary.content,
            },
            "sections": [
                section.to_dict() if hasattr(section, "to_dict") else section
                for section in self.sections
            ],
            "recommendations": [
                {
                    "title": item.title,
                    "content": item.content,
                    "priority": item.priority,
                }
                for item in self.recommendations
            ],
            "score": self.score,
            "appendix": self.appendix,
            "status": self.status.value if isinstance(self.status, ReportStatus) else self.status,
            "format": self.format.value if isinstance(self.format, ReportFormat) else self.format,
            "html": self.html,
            "markdown": self.markdown,
            "pdf_path": self.pdf_path,
            "templates_used": self.templates_used,
            "templates_unused": self.templates_unused,
            "template_coverage": self.template_coverage,
        }


# Public WP6 name
ReportModel = Report
