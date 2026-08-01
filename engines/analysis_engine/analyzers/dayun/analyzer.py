"""Dayun analyzer class skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.dayun.interfaces import DayunAnalyzerInterface
from engines.analysis_engine.analyzers.dayun.models import DayunAnalyzerResult
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class DayunAnalyzer(DayunAnalyzerInterface):
    """Architecture skeleton for the Dayun analyzer.

    Public interface only. No analysis logic.
    """

    analyzer_id: str = "dayun"
    version: str = "0.0.0"

    def analyze(self, context: PipelineContext) -> DayunAnalyzerResult:
        """Run analysis against the pipeline context."""
        raise NotImplementedError

    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""
        raise NotImplementedError
