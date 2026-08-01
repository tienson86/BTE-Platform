"""Liunian analyzer class skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.liunian.interfaces import LiunianAnalyzerInterface
from engines.analysis_engine.analyzers.liunian.models import LiunianAnalyzerResult
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class LiunianAnalyzer(LiunianAnalyzerInterface):
    """Architecture skeleton for the Liunian analyzer.

    Public interface only. No analysis logic.
    """

    analyzer_id: str = "liunian"
    version: str = "0.0.0"

    def analyze(self, context: PipelineContext) -> LiunianAnalyzerResult:
        """Run analysis against the pipeline context."""
        raise NotImplementedError

    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""
        raise NotImplementedError
