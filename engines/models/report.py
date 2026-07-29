"""
report.py
=========

Interpretation Report Model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .section import ReportSection
from .statistics import ReportStatistics


@dataclass(slots=True)
class InterpretationReport:
    """
    Báo cáo diễn giải hoàn chỉnh.
    """

    title: str = ""

    subtitle: str = ""

    summary: str = ""

    sections: list[ReportSection] = field(default_factory=list)

    appendix: list[str] = field(default_factory=list)

    statistics: ReportStatistics = field(
        default_factory=ReportStatistics
    )

    metadata: dict[str, Any] = field(default_factory=dict)

    version: str = "1.0"

    generated_at: datetime = field(
        default_factory=datetime.now
    )

    @property
    def section_count(self) -> int:
        return len(self.sections)

    def add_section(
        self,
        section: ReportSection,
    ) -> None:

        self.sections.append(section)
