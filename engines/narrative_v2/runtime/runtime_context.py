"""Narrative V2 runtime context and pipeline trace.

Object definitions only. No builder logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engines.narrative_v2.runtime.runtime_state import RuntimeState


@dataclass(slots=True)
class PipelineTraceEntry:
    """Single pipeline stage span. Builder independent."""

    stage: str
    started: float
    finished: float | None = None
    status: str = "running"

    def complete(self, *, finished: float, status: str) -> None:
        """Mark the span finished."""
        self.finished = finished
        self.status = status


@dataclass(slots=True)
class PipelineTrace:
    """Ordered pipeline trace. Not rendered to customers."""

    entries: list[PipelineTraceEntry] = field(default_factory=list)

    def start(self, stage: str, started: float) -> PipelineTraceEntry:
        """Open a stage span."""
        entry = PipelineTraceEntry(stage=stage, started=started)
        self.entries.append(entry)
        return entry

    def stages(self) -> tuple[str, ...]:
        """Executed stage names in order."""
        return tuple(entry.stage for entry in self.entries)

    def snapshot(self) -> "PipelineTrace":
        """Return a detached copy of current entries."""
        copied = [
            PipelineTraceEntry(
                stage=entry.stage,
                started=entry.started,
                finished=entry.finished,
                status=entry.status,
            )
            for entry in self.entries
        ]
        return PipelineTrace(entries=copied)


@dataclass(slots=True)
class NarrativeRuntimeContext:
    """Runtime session object.

    Fields only. Canonical analysis is stored, never interpreted.
    """

    canonical_analysis: object | None
    runtime_state: RuntimeState
    metadata: dict[str, Any]
    trace: PipelineTrace = field(default_factory=PipelineTrace)
    evidence: object | None = None
    reasoning: object | None = None
    knowledge: object | None = None
    rewrite: object | None = None
    summary: object | None = None
