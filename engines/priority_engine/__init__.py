"""BTE Priority Engine.

This package loads priority JSON data from the Knowledge Base, matches
activation conditions, plans execution order, resolves conflicts, and exposes
a small service API for the Interpretation Engine.
"""

from .condition_matcher import ConditionMatcher
from .exceptions import (
    PriorityConditionError,
    PriorityDataNotFoundError,
    PriorityDataValidationError,
    PriorityEngineError,
    PriorityResolutionError,
)
from .execution_planner import ExecutionPlanner
from .models import (
    ConditionMatch,
    ExecutionPlan,
    ExecutionStep,
    PriorityCondition,
    PriorityData,
    PriorityExample,
    PriorityLabel,
    PriorityPipelineResult,
    PriorityOrder,
    PriorityRule,
    ResolutionResult,
)
from .pipeline import PriorityPipeline
from .priority_resolver import PriorityResolver
from .rule_loader import PriorityRuleLoader
from .service import PriorityService

__all__ = [
    "ConditionMatch",
    "ConditionMatcher",
    "ExecutionPlan",
    "ExecutionPlanner",
    "ExecutionStep",
    "PriorityCondition",
    "PriorityConditionError",
    "PriorityData",
    "PriorityDataNotFoundError",
    "PriorityDataValidationError",
    "PriorityEngineError",
    "PriorityExample",
    "PriorityLabel",
    "PriorityOrder",
    "PriorityPipeline",
    "PriorityPipelineResult",
    "PriorityResolutionError",
    "PriorityResolver",
    "PriorityRule",
    "PriorityRuleLoader",
    "PriorityService",
    "ResolutionResult",
]
