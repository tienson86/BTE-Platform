"""Interpretation context lifecycle phase and revision models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ContextLifecyclePhase(str, Enum):
    """Pack 03 Interpretation Context lifecycle phases."""

    CREATED = "created"
    INITIALIZED = "initialized"
    EXPANDED = "expanded"
    VALIDATED = "validated"
    FINALIZED = "finalized"
    DISPOSED = "disposed"


@dataclass(frozen=True, slots=True)
class ContextRevision:
    """Immutable audit record for a single interpretation context revision."""

    revision_number: int
    context_id: str
    phase: ContextLifecyclePhase
    timestamp: str
    stage_id: str | None = None
    pipeline_run_id: str | None = None
    attribute_keys: tuple[str, ...] = ()
    messages: tuple[str, ...] = ()
