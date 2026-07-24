"""
Pattern Engine.

Điểm vào chính của Pattern Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from .context import PatternContext
from .service import PatternService


# Repo root: engines/pattern_engine/engine.py → parents[2]
_REPO_ROOT = Path(__file__).resolve().parents[2]

# Canonical Pattern Rule Database (WP1)
DEFAULT_DATABASE_PATH = str(_REPO_ROOT / "database" / "14_pattern")


@dataclass
class PatternResult:

    success: bool = True

    pattern: Optional[str] = None

    score: float = 0.0

    priority: int = 0

    matched_rules: List[str] = field(default_factory=list)

    error: Optional[str] = None


class PatternEngine:

    def __init__(
        self,
        database_path: str | None = None,
    ):

        self.database_path = database_path or DEFAULT_DATABASE_PATH

        self.service = PatternService(
            self.database_path
        )

    def calculate(
        self,
        context: PatternContext,
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
            ) or [],

            error=data.get(
                "error"
            )
        )

    def clear_cache(self):

        self.service.clear_cache()
