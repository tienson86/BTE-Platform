"""
Pattern Engine.

Điểm vào chính của Pattern Engine.
"""

from dataclasses import dataclass
from typing import List, Optional

from .context import PatternContext
from .service import PatternService


@dataclass
class PatternResult:

    success: bool = True

    pattern: Optional[str] = None

    score: float = 0.0

    priority: int = 0

    matched_rules: List[str] = None

    error: Optional[str] = None


class PatternEngine:

    def __init__(self,
                 database_path="database/04_pattern"):

        self.service = PatternService(
            database_path
        )

    def calculate(
        self,
        context: PatternContext
    ) -> PatternResult:

        data = self.service.analyze(
            context
        )

        return PatternResult(

            success=data.get(
                "success",
                False
            ),

            pattern=data.get(
                "pattern"
            ),

            score=data.get(
                "score",
                0
            ),

            priority=data.get(
                "priority",
                0
            ),

            matched_rules=data.get(
                "matched_rules",
                []
            ),

            error=data.get(
                "error"
            )
        )

    def clear_cache(self):

        self.service.clear_cache()
