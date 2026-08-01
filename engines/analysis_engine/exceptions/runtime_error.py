"""Runtime-related Analysis Engine exceptions."""

from __future__ import annotations

from engines.analysis_engine.exceptions.analysis_error import AnalysisError


class AnalysisRuntimeError(AnalysisError):
    """Raised for Analysis Engine runtime execution failures.

    Named ``AnalysisRuntimeError`` to avoid shadowing the builtin ``RuntimeError``.
    """
