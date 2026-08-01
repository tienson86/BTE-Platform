"""Scoring analyzer class skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.scoring.interfaces import ScoringAnalyzerInterface
from engines.analysis_engine.analyzers.scoring.models import ScoringAnalyzerResult
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class ScoringAnalyzer(ScoringAnalyzerInterface):
    """Architecture skeleton for the Scoring analyzer.

    Public interface only. No analysis logic.
    """

    analyzer_id: str = "scoring"
    version: str = "0.0.0"

    def analyze(self, context: PipelineContext) -> ScoringAnalyzerResult:
        """Run analysis against the pipeline context."""
        raise NotImplementedError

    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""
        raise NotImplementedError
