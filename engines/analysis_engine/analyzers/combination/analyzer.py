"""Combination analyzer class skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.combination.interfaces import CombinationAnalyzerInterface
from engines.analysis_engine.analyzers.combination.models import CombinationAnalyzerResult
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class CombinationAnalyzer(CombinationAnalyzerInterface):
    """Architecture skeleton for the Combination analyzer.

    Public interface only. No analysis logic.
    """

    analyzer_id: str = "combination"
    version: str = "0.0.0"

    def analyze(self, context: PipelineContext) -> CombinationAnalyzerResult:
        """Run analysis against the pipeline context."""
        raise NotImplementedError

    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""
        raise NotImplementedError
