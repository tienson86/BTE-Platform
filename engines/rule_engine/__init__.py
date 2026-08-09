"""
BTE Rule Engine

Canonical infrastructure for loading, validating, indexing, matching and
prioritizing analytical rules.

Reuses Rule Contract V1 for condition evaluation.
Does not own analytical knowledge or mutate rule data files.
"""

from __future__ import annotations

from engines.rule_engine.cache import RuleCache
from engines.rule_engine.engine import RuleEngine
from engines.rule_engine.exceptions import (
    RuleEngineError,
    RuleLoadError,
    RuleValidationError,
)
from engines.rule_engine.loader import RuleLoader
from engines.rule_engine.matcher import RuleMatcher
from engines.rule_engine.models import (
    EngineStatistics,
    LoadResult,
    MatchResult,
    RuleRecord,
    ValidationDiagnostic,
)
from engines.rule_engine.priority import PriorityResolver
from engines.rule_engine.registry import RuleRegistry
from engines.rule_engine.validator import RuleValidator

__all__ = [
    "EngineStatistics",
    "LoadResult",
    "MatchResult",
    "PriorityResolver",
    "RuleCache",
    "RuleEngine",
    "RuleEngineError",
    "RuleLoadError",
    "RuleLoader",
    "RuleMatcher",
    "RuleRecord",
    "RuleRegistry",
    "RuleValidationError",
    "RuleValidator",
    "ValidationDiagnostic",
]

__version__ = "1.0.0"
