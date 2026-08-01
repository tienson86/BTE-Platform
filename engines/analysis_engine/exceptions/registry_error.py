"""Registry-related Analysis Engine exceptions."""

from __future__ import annotations

from engines.analysis_engine.exceptions.analysis_error import AnalysisError


class RegistryError(AnalysisError):
    """Raised for registry lookup, resolve, or compatibility failures."""
