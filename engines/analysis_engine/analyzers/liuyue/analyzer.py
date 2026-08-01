"""Liuyue analyzer class skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.liuyue.interfaces import LiuyueAnalyzerInterface
from engines.analysis_engine.analyzers.liuyue.models import LiuyueAnalyzerResult
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class LiuyueAnalyzer(LiuyueAnalyzerInterface):
    """Architecture skeleton for the Liuyue analyzer.

    Public interface only. No analysis logic.
    """

    analyzer_id: str = "liuyue"
    version: str = "0.0.0"

    def analyze(self, context: PipelineContext) -> LiuyueAnalyzerResult:
        """Run analysis against the pipeline context."""
        raise NotImplementedError

    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""
        raise NotImplementedError
