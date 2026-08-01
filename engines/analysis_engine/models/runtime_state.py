"""Runtime state model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps


@dataclass(frozen=True, slots=True)
class RuntimeState:
    """Immutable runtime execution state contract."""

    id: str
    version: str
    metadata: AnalysisMetadata
    trace: tuple[str, ...]
    timestamps: ModelTimestamps
    runtime_id: str
    status: str
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate runtime state contract."""
        raise NotImplementedError
