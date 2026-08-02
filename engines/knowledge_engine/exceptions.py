"""Knowledge Engine exceptions."""

from __future__ import annotations


class KnowledgeEngineError(Exception):
    """Base error for the Knowledge Engine."""


class KnowledgeSchemaError(KnowledgeEngineError):
    """Raised when a knowledge CSV fails schema validation."""


class KnowledgeLoadError(KnowledgeEngineError):
    """Raised when knowledge CSV files cannot be loaded."""
