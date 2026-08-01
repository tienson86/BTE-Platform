"""Shared status enums, literals, and typed dicts."""

from __future__ import annotations

from enum import Enum
from typing import Literal, TypedDict


class LifecycleStatus(str, Enum):
    """Lifecycle status values for analysis artifacts."""

    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    RETIRED = "retired"
    FROZEN = "frozen"


class ExecutionStatus(str, Enum):
    """Execution status values for pipeline and runtime states."""

    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PARTIAL = "partial"


StatusLiteral = Literal[
    "draft",
    "active",
    "deprecated",
    "retired",
    "frozen",
    "pending",
    "ready",
    "running",
    "succeeded",
    "failed",
    "cancelled",
    "partial",
]


class StatusPayload(TypedDict):
    """Status payload contract."""

    status: StatusLiteral
    message: str | None
