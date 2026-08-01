"""Analysis evidence model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps


@dataclass(frozen=True, slots=True)
class AnalysisEvidence:
    """Immutable evidence contract supporting analysis decisions."""

    id: str
    version: str
    metadata: AnalysisMetadata
    trace: tuple[str, ...]
    timestamps: ModelTimestamps
    source: str
    reference_ids: tuple[str, ...] = ()
    payload: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate analysis evidence contract."""
        raise NotImplementedError
