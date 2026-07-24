"""
Pattern Service.

Cung cấp API cho các Engine khác.
"""

from __future__ import annotations

from pathlib import Path

from .calculator import PatternCalculator
from .loader import PatternLoader

# Keep default aligned with engine.DEFAULT_DATABASE_PATH
_REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE_PATH = str(_REPO_ROOT / "database" / "14_pattern")


class PatternService:

    def __init__(
        self,
        database_path: str | None = None,
    ):

        path = database_path or DEFAULT_DATABASE_PATH

        self.loader = PatternLoader(
            path
        )

        self.calculator = PatternCalculator(
            self.loader
        )

    def analyze(self, context):

        return self.calculator.calculate(
            context
        )

    def clear_cache(self):

        self.loader.clear_cache()

    def cache_size(self):

        return self.loader.cache_size()
