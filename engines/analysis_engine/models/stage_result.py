"""Stage result model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.analysis_decision import AnalysisDecision
from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps
from engines.analysis_engine.models.analysis_score import AnalysisScore


@dataclass(frozen=True, slots=True)
class StageResult:
    """Immutable stage result contract."""

    id: str
    version: str
    metadata: AnalysisMetadata
    trace: tuple[str, ...]
    timestamps: ModelTimestamps
    stage_id: str
    success: bool
    scores: tuple[AnalysisScore, ...] = ()
    decisions: tuple[AnalysisDecision, ...] = ()
    payload: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate stage result contract."""
        raise NotImplementedError
