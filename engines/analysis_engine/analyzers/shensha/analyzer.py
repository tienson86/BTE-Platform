"""Shen Sha analyzer class skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.shensha.interfaces import ShenshaAnalyzerInterface
from engines.analysis_engine.analyzers.shensha.models import ShenshaAnalyzerResult
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class ShenshaAnalyzer(ShenshaAnalyzerInterface):
    """Architecture skeleton for the Shen Sha analyzer.

    Public interface only. No analysis logic.
    """

    analyzer_id: str = "shensha"
    version: str = "0.0.0"

    def analyze(self, context: PipelineContext) -> ShenshaAnalyzerResult:
        """Run analysis against the pipeline context."""
        raise NotImplementedError

    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""
        raise NotImplementedError
