"""
engines.pattern — compatibility package.

.. deprecated:: WP1
    Stub removed. Engine/Result/Context delegate to ``engines.pattern_engine``.
    Local calculator/matcher kept for backward compatibility.
"""

from engines.pattern_engine.context import PatternContext
from engines.pattern_engine.engine import PatternEngine, PatternResult

from .calculator import PatternCalculator
from .matcher import PatternMatcher

__all__ = [
    "PatternEngine",
    "PatternResult",
    "PatternContext",
    "PatternCalculator",
    "PatternMatcher",
]
