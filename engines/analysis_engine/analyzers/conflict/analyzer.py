"""Conflict analyzer class skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.conflict.interfaces import ConflictAnalyzerInterface
from engines.analysis_engine.analyzers.conflict.models import ConflictAnalyzerResult
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class ConflictAnalyzer(ConflictAnalyzerInterface):
    """Architecture skeleton for the Conflict analyzer.

    Public interface only. No analysis logic.
    """

    analyzer_id: str = "conflict"
    version: str = "0.0.0"

    def analyze(self, context: PipelineContext) -> ConflictAnalyzerResult:
        """Run analysis against the pipeline context."""
        raise NotImplementedError

    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""
        raise NotImplementedError
