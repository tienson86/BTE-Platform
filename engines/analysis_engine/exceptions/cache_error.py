"""Cache-related Analysis Engine exceptions."""

from __future__ import annotations

from engines.analysis_engine.exceptions.analysis_error import AnalysisError


class CacheError(AnalysisError):
    """Raised for Analysis Engine in-memory cache policy or access failures."""
