"""Analysis context revision model for lifecycle auditing."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ContextLifecyclePhase(str, Enum):
    """Pack 02 Analysis Context lifecycle phases."""

    CREATED = "created"
    INITIALIZED = "initialized"
    EXPANDED = "expanded"
    VALIDATED = "validated"
    FINALIZED = "finalized"
    DISPOSED = "disposed"


@dataclass(frozen=True, slots=True)
class ContextRevision:
    """Immutable audit record for a single context revision.

    Records lifecycle metadata only. Does not evaluate analyzer logic.
    """

    revision_number: int
    context_id: str
    phase: ContextLifecyclePhase
    timestamp: str
    stage_id: str | None = None
    analyzer_id: str | None = None
    pipeline_run_id: str | None = None
    attribute_keys: tuple[str, ...] = ()
    messages: tuple[str, ...] = ()
