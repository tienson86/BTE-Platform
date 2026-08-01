"""Module result model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.analysis_decision import AnalysisDecision
from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps
from engines.analysis_engine.models.analysis_score import AnalysisScore
from engines.analysis_engine.models.stage_result import StageResult


@dataclass(frozen=True, slots=True)
class ModuleResult:
    """Immutable analyzer/module result contract."""

    id: str
    version: str
    metadata: AnalysisMetadata
    trace: tuple[str, ...]
    timestamps: ModelTimestamps
    module_id: str
    success: bool
    stage_results: tuple[StageResult, ...] = ()
    scores: tuple[AnalysisScore, ...] = ()
    decisions: tuple[AnalysisDecision, ...] = ()
    payload: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate module result contract."""
        raise NotImplementedError
