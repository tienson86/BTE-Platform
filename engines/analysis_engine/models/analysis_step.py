"""Analysis step model."""

from __future__ import annotations

from dataclasses import dataclass

from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps


@dataclass(frozen=True, slots=True)
class AnalysisStep:
    """Immutable pipeline step contract."""

    id: str
    version: str
    metadata: AnalysisMetadata
    trace: tuple[str, ...]
    timestamps: ModelTimestamps
    name: str
    status: str
    order: int = 0

    def validate(self) -> bool:
        """Validate analysis step contract."""
        raise NotImplementedError
