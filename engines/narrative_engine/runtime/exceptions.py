"""Narrative Runtime exceptions (Sprint D1)."""

from __future__ import annotations


class NarrativeRuntimeError(Exception):
    """Base error for Narrative Runtime (tree composition)."""


class NarrativeRuntimeValidationError(NarrativeRuntimeError):
    """Input or tree integrity validation failed."""
