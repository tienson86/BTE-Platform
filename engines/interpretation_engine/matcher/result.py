from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class MatchResult:
    """
    Kết quả Match một Rule.
    """

    matched: bool

    score: float = 0.0

    priority: int = 0

    reason: str = ""

    rule_id: str = ""

    template_id: str = ""

    data: dict = field(default_factory=dict)
