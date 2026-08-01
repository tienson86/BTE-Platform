"""Analysis context model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps


@dataclass(frozen=True, slots=True)
class AnalysisContext:
    """Immutable shared analysis context contract."""

    id: str
    version: str
    metadata: AnalysisMetadata
    trace: tuple[str, ...]
    timestamps: ModelTimestamps
    pipeline_id: str
    chart_id: str | None = None
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate analysis context contract."""
        raise NotImplementedError
