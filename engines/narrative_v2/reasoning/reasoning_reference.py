"""Traceability pointer for a reasoning node or edge."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReasoningReference:
    """Internal trace pointer. Not customer-facing."""

    source: str
    kind: str
