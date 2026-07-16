"""
Pattern Result Model.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PatternResultModel:

    success: bool = True

    pattern: Optional[str] = None

    score: float = 0.0

    priority: int = 0

    matched_rules: List[str] = field(default_factory=list)

    follow_pattern: bool = False

    special_pattern: bool = False

    description: str = ""

    error: Optional[str] = None
