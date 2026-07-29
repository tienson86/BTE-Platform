"""
section.py
==========

Report Section Model.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .paragraph import ReportParagraph


@dataclass(slots=True)
class ReportSection:
    """
    Một chương của báo cáo.
    """

    title: str

    description: str = ""

    paragraphs: list[ReportParagraph] = field(default_factory=list)

    rule_count: int = 0

    order: int = 0

    @property
    def paragraph_count(self) -> int:
        return len(self.paragraphs)

    def add_paragraph(
        self,
        paragraph: ReportParagraph,
    ) -> None:

        self.paragraphs.append(paragraph)
