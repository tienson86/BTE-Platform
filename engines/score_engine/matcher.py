"""
Rule Matcher (legacy module path).

WP2B-2: re-export Score matcher facade — no eval().
"""

from engines.score_engine.matcher.matcher import RuleMatcher

__all__ = ["RuleMatcher"]
