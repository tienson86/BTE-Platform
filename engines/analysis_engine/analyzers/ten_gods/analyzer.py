"""Ten Gods analyzer class skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.ten_gods.interfaces import TenGodsAnalyzerInterface
from engines.analysis_engine.analyzers.ten_gods.models import TenGodsAnalyzerResult
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class TenGodsAnalyzer(TenGodsAnalyzerInterface):
    """Architecture skeleton for the Ten Gods analyzer.

    Public interface only. No analysis logic.
    """

    analyzer_id: str = "ten_gods"
    version: str = "0.0.0"

    def analyze(self, context: PipelineContext) -> TenGodsAnalyzerResult:
        """Run analysis against the pipeline context."""
        raise NotImplementedError

    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""
        raise NotImplementedError
