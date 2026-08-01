"""Interpretation context snapshot model for lifecycle persistence."""

from __future__ import annotations

from dataclasses import dataclass

from engines.interpretation_engine.context.interpretation_context import InterpretationContext
from engines.interpretation_engine.context.revision import ContextLifecyclePhase


@dataclass(frozen=True, slots=True)
class ContextSnapshot:
    """Immutable snapshot of an Interpretation Context at a lifecycle point."""

    snapshot_id: str
    context_id: str
    phase: ContextLifecyclePhase
    revision_number: int
    context: InterpretationContext
    created_at: str
    label: str | None = None
