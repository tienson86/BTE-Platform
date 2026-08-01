"""Pattern analyzer class skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.pattern.interfaces import PatternAnalyzerInterface
from engines.analysis_engine.analyzers.pattern.models import PatternAnalyzerResult
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class PatternAnalyzer(PatternAnalyzerInterface):
    """Architecture skeleton for the Pattern analyzer.

    Public interface only. No analysis logic.
    """

    analyzer_id: str = "pattern"
    version: str = "0.0.0"

    def analyze(self, context: PipelineContext) -> PatternAnalyzerResult:
        """Run analysis against the pipeline context."""
        raise NotImplementedError

    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""
        raise NotImplementedError
