"""Pipeline-related Analysis Engine exceptions."""

from __future__ import annotations

from engines.analysis_engine.exceptions.analysis_error import AnalysisError


class PipelineError(AnalysisError):
    """Raised for pipeline orchestration or stage execution failures."""
