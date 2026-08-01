"""Analysis result model skeleton."""

from __future__ import annotations

from dataclasses import dataclass

from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata
from engines.analysis_engine.models.analysis_score import AnalysisScore
from engines.analysis_engine.models.analysis_step import AnalysisStep


@dataclass(slots=True)
class AnalysisResult:
    """Final analysis result contract."""

    pipeline_id: str
    success: bool
    steps: tuple[AnalysisStep, ...]
    scores: tuple[AnalysisScore, ...]
    metadata: AnalysisMetadata | None = None
