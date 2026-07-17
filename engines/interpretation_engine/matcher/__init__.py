"""
BTE Platform
Interpretation Engine

Matcher Package
"""

from .context import MatchContext
from .result import MatchResult

from .rule_matcher import RuleMatcher
from .condition_evaluator import ConditionEvaluator

from .priority_resolver import PriorityResolver
from .conflict_resolver import ConflictResolver

__all__ = [
    "MatchContext",
    "MatchResult",
    "RuleMatcher",
    "ConditionEvaluator",
    "PriorityResolver",
    "ConflictResolver",
]
