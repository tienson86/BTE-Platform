"""
sentence.py
===========

Report Sentence Model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ReportSentence:
    """
    Một câu trong báo cáo.
    """

    text: str

    rule_id: str = ""

    category: str = ""

    topic: str = ""

    score: float = 0.0

    priority: int = 0

    confidence: float = 1.0

    metadata: dict[str, Any] = field(default_factory=dict)
