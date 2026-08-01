"""Useful God analyzer class skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.useful_god.interfaces import UsefulGodAnalyzerInterface
from engines.analysis_engine.analyzers.useful_god.models import UsefulGodAnalyzerResult
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class UsefulGodAnalyzer(UsefulGodAnalyzerInterface):
    """Architecture skeleton for the Useful God analyzer.

    Public interface only. No analysis logic.
    """

    analyzer_id: str = "useful_god"
    version: str = "0.0.0"

    def analyze(self, context: PipelineContext) -> UsefulGodAnalyzerResult:
        """Run analysis against the pipeline context."""
        raise NotImplementedError

    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""
        raise NotImplementedError
