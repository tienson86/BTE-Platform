"""Interpretation output trace information model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class TraceInformation:
    """Immutable trace contract for Pack 03 interpretation outputs.

    Records structural execution trail identifiers only. No report rendering.
    """

    trace_id: str
    pipeline_id: str = ""
    source_final_result_id: str = ""
    stage_ids: tuple[str, ...] = ()
    interpreter_ids: tuple[str, ...] = ()
    events: tuple[str, ...] = ()
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate trace information structural integrity."""
        return bool(self.trace_id)

    def with_event(self, event: str) -> TraceInformation:
        """Return a new trace with an appended event identifier."""
        return TraceInformation(
            trace_id=self.trace_id,
            pipeline_id=self.pipeline_id,
            source_final_result_id=self.source_final_result_id,
            stage_ids=self.stage_ids,
            interpreter_ids=self.interpreter_ids,
            events=self.events + (event,),
            attributes=dict(self.attributes),
        )
