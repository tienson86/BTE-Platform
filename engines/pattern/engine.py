"""
Compatibility facade.

Delegates to ``engines.pattern_engine.engine`` (WP1 Pattern Recovery).
"""

from engines.pattern_engine.engine import PatternEngine, PatternResult

__all__ = ["PatternEngine", "PatternResult"]
