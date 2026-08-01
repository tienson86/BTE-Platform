"""Context-related Analysis Engine exceptions."""

from __future__ import annotations

from engines.analysis_engine.exceptions.analysis_error import AnalysisError


class ContextError(AnalysisError):
    """Raised for analysis context contract or lifecycle failures."""
