"""Analysis score model."""

from __future__ import annotations

from dataclasses import dataclass

from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps


@dataclass(frozen=True, slots=True)
class AnalysisScore:
    """Immutable score value contract for analysis outputs."""

    id: str
    version: str
    metadata: AnalysisMetadata
    trace: tuple[str, ...]
    timestamps: ModelTimestamps
    dimension: str
    value: float
    unit: str | None = None

    def validate(self) -> bool:
        """Validate analysis score contract."""
        raise NotImplementedError
