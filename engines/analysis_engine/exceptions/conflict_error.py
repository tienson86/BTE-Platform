"""Conflict-related Analysis Engine exceptions."""

from __future__ import annotations

from engines.analysis_engine.exceptions.analysis_error import AnalysisError


class ConflictError(AnalysisError):
    """Raised for analysis conflict detection or resolution failures."""
