"""
Rule Engine.
"""

from .engine import RuleEngine
from pathlib import Path


class RuleLoader:
    def load(self, path):
        return [] if Path(path).is_dir() else []


__all__ = ["RuleEngine", "RuleLoader"]
