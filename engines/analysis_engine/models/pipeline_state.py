"""Pipeline state model."""

from __future__ import annotations

from dataclasses import dataclass

from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps


@dataclass(frozen=True, slots=True)
class PipelineState:
    """Immutable pipeline execution state contract."""

    id: str
    version: str
    metadata: AnalysisMetadata
    trace: tuple[str, ...]
    timestamps: ModelTimestamps
    pipeline_id: str
    status: str
    current_stage_id: str | None = None
    completed_stage_ids: tuple[str, ...] = ()

    def validate(self) -> bool:
        """Validate pipeline state contract."""
        raise NotImplementedError
