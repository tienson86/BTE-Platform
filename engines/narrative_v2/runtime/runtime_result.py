"""Narrative V2 runtime result object.

Presentation is the frozen internal contract. Not production customer publish.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.narrative_v2.runtime.runtime_context import PipelineTrace


@dataclass(slots=True)
class NarrativeRuntimeResult:
    """Runtime result. Presentation is set only after internal freeze."""

    status: str
    runtime_metadata: Mapping[str, Any]
    pipeline_trace: PipelineTrace
    presentation: object | None
    errors: tuple[str, ...]
