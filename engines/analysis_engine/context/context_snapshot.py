"""Analysis context snapshot model for lifecycle persistence."""

from __future__ import annotations

from dataclasses import dataclass

from engines.analysis_engine.context.context_revision import ContextLifecyclePhase
from engines.analysis_engine.models.analysis_context import AnalysisContext


@dataclass(frozen=True, slots=True)
class ContextSnapshot:
    """Immutable snapshot of an Analysis Context at a lifecycle point.

    Snapshots are the only persistence form for context state.
    """

    snapshot_id: str
    context_id: str
    phase: ContextLifecyclePhase
    revision_number: int
    context: AnalysisContext
    created_at: str
    label: str | None = None
