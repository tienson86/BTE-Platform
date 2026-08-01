"""Final result model."""

from __future__ import annotations

from dataclasses import dataclass

from engines.analysis_engine.models.analysis_decision import AnalysisDecision
from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps
from engines.analysis_engine.models.analysis_result import AnalysisResult
from engines.analysis_engine.models.analysis_score import AnalysisScore
from engines.analysis_engine.models.module_result import ModuleResult


@dataclass(frozen=True, slots=True)
class FinalResult:
    """Immutable final aggregated analysis result contract."""

    id: str
    version: str
    metadata: AnalysisMetadata
    trace: tuple[str, ...]
    timestamps: ModelTimestamps
    pipeline_id: str
    success: bool
    analysis_result: AnalysisResult | None = None
    module_results: tuple[ModuleResult, ...] = ()
    scores: tuple[AnalysisScore, ...] = ()
    decisions: tuple[AnalysisDecision, ...] = ()
    summary_codes: tuple[str, ...] = ()

    def validate(self) -> bool:
        """Validate final result contract."""
        raise NotImplementedError
