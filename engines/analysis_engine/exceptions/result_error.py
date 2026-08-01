"""Result-related Analysis Engine exceptions."""

from __future__ import annotations

from engines.analysis_engine.exceptions.analysis_error import AnalysisError


class ResultError(AnalysisError):
    """Raised for analysis result construction, merge, or persistence failures."""
