"""Analysis context model skeleton."""

from __future__ import annotations

from dataclasses import dataclass

from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata


@dataclass(slots=True)
class AnalysisContext:
    """Shared immutable analysis context contract."""

    context_id: str
    pipeline_id: str
    chart_id: str | None = None
    metadata: AnalysisMetadata | None = None
