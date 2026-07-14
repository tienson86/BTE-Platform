"""
rule_result.py
==============

Kết quả sau khi một Rule được áp dụng.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any

from .rule import Rule


@dataclass(slots=True)
class RuleResult:

    rule: Rule

    matched: bool

    score: float = 0.0

    priority: int = 0

    text: str = ""

    variables: Dict[str, Any] = field(default_factory=dict)

    explanation: str = ""

    def is_success(self):

        return self.matched
