"""Temperature analyzer class skeleton."""

from __future__ import annotations

from engines.analysis_engine.analyzers.temperature.interfaces import TemperatureAnalyzerInterface
from engines.analysis_engine.analyzers.temperature.models import TemperatureAnalyzerResult
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class TemperatureAnalyzer(TemperatureAnalyzerInterface):
    """Architecture skeleton for the Temperature analyzer.

    Public interface only. No analysis logic.
    """

    analyzer_id: str = "temperature"
    version: str = "0.0.0"

    def analyze(self, context: PipelineContext) -> TemperatureAnalyzerResult:
        """Run analysis against the pipeline context."""
        raise NotImplementedError

    def supports(self, context: PipelineContext) -> bool:
        """Indicate whether this analyzer supports the context."""
        raise NotImplementedError
