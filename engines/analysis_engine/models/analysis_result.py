"""Analysis result model."""

from __future__ import annotations

from dataclasses import dataclass

from engines.analysis_engine.models.analysis_decision import AnalysisDecision
from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps
from engines.analysis_engine.models.analysis_score import AnalysisScore
from engines.analysis_engine.models.module_result import ModuleResult
from engines.analysis_engine.models.stage_result import StageResult


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    """Immutable analysis result contract."""

    id: str
    version: str
    metadata: AnalysisMetadata
    trace: tuple[str, ...]
    timestamps: ModelTimestamps
    pipeline_id: str
    success: bool
    stage_results: tuple[StageResult, ...] = ()
    module_results: tuple[ModuleResult, ...] = ()
    scores: tuple[AnalysisScore, ...] = ()
    decisions: tuple[AnalysisDecision, ...] = ()

    def validate(self) -> bool:
        """Validate analysis result contract."""
        raise NotImplementedError
