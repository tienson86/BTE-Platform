"""Shared severity enums, literals, and typed dicts."""

from __future__ import annotations

from enum import Enum
from typing import Literal, TypedDict


class Severity(str, Enum):
    """Severity levels for validation and runtime findings."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


SeverityLiteral = Literal["info", "low", "medium", "high", "critical"]


class SeverityPayload(TypedDict):
    """Severity payload contract."""

    severity: SeverityLiteral
    code: str
    message: str
