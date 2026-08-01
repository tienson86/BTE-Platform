"""Decision-related Analysis Engine exceptions."""

from __future__ import annotations

from engines.analysis_engine.exceptions.analysis_error import AnalysisError


class DecisionError(AnalysisError):
    """Raised for analysis decision contract or consistency failures."""
