"""Validation-related Analysis Engine exceptions."""

from __future__ import annotations

from engines.analysis_engine.exceptions.analysis_error import AnalysisError


class ValidationError(AnalysisError):
    """Raised for schema, metadata, or contract validation failures."""
