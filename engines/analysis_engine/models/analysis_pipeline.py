"""Analysis pipeline model."""

from __future__ import annotations

from dataclasses import dataclass

from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps
from engines.analysis_engine.models.analysis_step import AnalysisStep


@dataclass(frozen=True, slots=True)
class AnalysisPipeline:
    """Immutable pipeline definition contract."""

    id: str
    version: str
    metadata: AnalysisMetadata
    trace: tuple[str, ...]
    timestamps: ModelTimestamps
    name: str
    steps: tuple[AnalysisStep, ...] = ()

    def validate(self) -> bool:
        """Validate analysis pipeline contract."""
        raise NotImplementedError
