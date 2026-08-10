"""Log stream contract. No logging framework changes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

LogStreamKind = Literal[
    "application",
    "access",
    "error",
    "audit",
    "security",
    "operational",
]


@dataclass(slots=True, frozen=True)
class LogStreamContract:
    """One standardized log stream."""

    kind: LogStreamKind
    name: str
    owner: str
    destination: str
    contains_pii: bool = False
    format_hint: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
