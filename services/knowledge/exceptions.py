"""Knowledge infrastructure exceptions."""

from __future__ import annotations


class KnowledgeError(Exception):
    """Base error for Knowledge infrastructure."""


class KnowledgeLoadError(KnowledgeError):
    """Raised when schemas or records cannot be loaded."""


class KnowledgeValidationError(KnowledgeError):
    """Raised when validation fails fatally."""


class KnowledgeSchemaError(KnowledgeValidationError):
    """Raised when schema resolution or schema validation fails."""


class KnowledgeIndexError(KnowledgeError):
    """Raised when index construction fails."""


class KnowledgeQueryError(KnowledgeError):
    """Raised when search/list queries are invalid."""


class KnowledgeExportError(KnowledgeError):
    """Raised when export IO fails."""
