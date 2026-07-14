"""
rule_result.py
==============

Kết quả sau khi Rule được đánh giá.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .rule import Rule


@dataclass(slots=True)
class RuleResult:
    """
    Kết quả đánh giá Rule.
    """

    rule: Rule

    matched: bool

    priority: int = 0

    score: float = 0.0

    text: str = ""

    confidence: float = 1.0

    explanation: str = ""

    # =====================================================
    # Metadata copy từ Rule
    # =====================================================

    module: str = ""

    category: str = ""

    topic: str = ""

    section: str = ""

    tags: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """
        Đồng bộ metadata từ Rule.
        """

        self.module = self.rule.module
        self.category = self.rule.category
        self.topic = self.rule.topic
        self.section = self.rule.section
        self.tags = list(self.rule.tags)
        self.metadata = dict(self.rule.metadata)
