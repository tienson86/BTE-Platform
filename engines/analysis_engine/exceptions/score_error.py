"""Score-related Analysis Engine exceptions."""

from __future__ import annotations

from engines.analysis_engine.exceptions.analysis_error import AnalysisError


class ScoreError(AnalysisError):
    """Raised for analysis score contract or consistency failures."""
