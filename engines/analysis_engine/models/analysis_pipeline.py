"""Analysis pipeline model skeleton."""

from __future__ import annotations

from dataclasses import dataclass

from engines.analysis_engine.models.analysis_step import AnalysisStep


@dataclass(slots=True)
class AnalysisPipeline:
    """Pipeline definition contract."""

    pipeline_id: str
    name: str
    steps: tuple[AnalysisStep, ...]
    version: str = "0.0.0"
