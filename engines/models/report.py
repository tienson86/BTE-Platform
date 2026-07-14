"""
report.py
=========

Model kết quả cuối cùng của Interpretation Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .rule_result import RuleResult


@dataclass(slots=True)
class InterpretationReport:

    title: str = ""

    summary: str = ""

    sections: List[str] = field(default_factory=list)

    rule_results: List[RuleResult] = field(default_factory=list)

    score: float = 0.0

    version: str = "1.0"

    def add_section(self, text: str):

        self.sections.append(text)

    def add_result(self, result: RuleResult):

        self.rule_results.append(result)

    @property
    def total_rules(self):

        return len(self.rule_results)
@dataclass(slots=True)
class ReportParagraph:

    title: str

    sentences: list[str] = field(default_factory=list)

    rule_count: int = 0


@dataclass(slots=True)
class ReportSection:

    title: str

    paragraphs: list[ReportParagraph] = field(default_factory=list)

    rule_count: int = 0
