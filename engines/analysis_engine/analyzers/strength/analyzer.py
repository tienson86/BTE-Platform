"""Strength analyzer class skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.strength.interfaces import StrengthAnalyzerInterface
from engines.analysis_engine.analyzers.strength.models import StrengthAnalyzerResult
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class StrengthAnalyzer(StrengthAnalyzerInterface):
    """Architecture skeleton for the Strength analyzer.

    Public interface only. No analysis logic.
    """

    analyzer_id: str = "strength"
    version: str = "0.0.0"

    def analyze(self, context: PipelineContext) -> StrengthAnalyzerResult:
        """Run analysis against the pipeline context."""
        raise NotImplementedError

    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""
        raise NotImplementedError
