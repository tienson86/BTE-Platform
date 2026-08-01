"""Shared priority enums, literals, and typed dicts."""

from __future__ import annotations

from enum import Enum
from typing import Literal, TypedDict, TypeAlias

PriorityValue: TypeAlias = int


class PriorityLevel(str, Enum):
    """Discrete priority levels."""

    LOWEST = "lowest"
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    HIGHEST = "highest"


PriorityLiteral = Literal["lowest", "low", "normal", "high", "highest"]


class PriorityPayload(TypedDict):
    """Priority payload contract."""

    level: PriorityLiteral
    value: PriorityValue
    source: str | None
