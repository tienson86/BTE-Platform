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

    subtitle: str = ""

    summary: str = ""

    sections: list[ReportSection] = field(default_factory=list)

    appendix: list[str] = field(default_factory=list)

    statistics: dict = field(default_factory=dict)

    metadata: dict = field(default_factory=dict)

    version: str = ""

    generated_at: datetime | None = None
