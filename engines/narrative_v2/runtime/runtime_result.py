"""Narrative V2 runtime result object.

Fields only. No narrative content.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.narrative_v2.runtime.runtime_context import PipelineTrace


@dataclass(slots=True)
class NarrativeRuntimeResult:
    """Skeleton runtime result. Presentation is empty in N-IMP-01."""

    status: str
    runtime_metadata: Mapping[str, Any]
    pipeline_trace: PipelineTrace
    presentation: None
    errors: tuple[str, ...]
