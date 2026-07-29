"""
Pattern Rule Model.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PatternRule:

    rule_id: str

    pattern: str

    priority: int = 0

    score: float = 0.0

    conditions: list[Any] = field(default_factory=list)

    description: str = ""

    enabled: bool = True

    source: str = ""
