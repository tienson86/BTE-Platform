"""Central shared enums for the Analysis Engine type system."""

from __future__ import annotations

from enum import Enum

from engines.analysis_engine.types.categories import AnalysisCategory
from engines.analysis_engine.types.priority import PriorityLevel
from engines.analysis_engine.types.severity import Severity
from engines.analysis_engine.types.status import ExecutionStatus, LifecycleStatus


class DecisionOutcome(str, Enum):
    """Canonical decision outcome values."""

    ACCEPT = "accept"
    REJECT = "reject"
    DEFER = "defer"
    OVERRIDE = "override"


class ResultKind(str, Enum):
    """Canonical result kind values."""

    STAGE = "stage"
    MODULE = "module"
    ANALYSIS = "analysis"
    FINAL = "final"
    EXECUTION = "execution"
    FAILURE = "failure"


class ObjectType(str, Enum):
    """Canonical registry-compatible object types."""

    CONTEXT = "context"
    RULE = "rule"
    SCORE = "score"
    DECISION = "decision"
    EVIDENCE = "evidence"
    PIPELINE = "pipeline"
    STAGE = "stage"
    ANALYZER = "analyzer"
    SCHEMA = "schema"
    METADATA = "metadata"


__all__ = [
    "AnalysisCategory",
    "DecisionOutcome",
    "ExecutionStatus",
    "LifecycleStatus",
    "ObjectType",
    "PriorityLevel",
    "ResultKind",
    "Severity",
]
