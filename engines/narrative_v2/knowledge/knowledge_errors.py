"""Narrative V2 Knowledge error model.

N-IMP-04: resolution and validation failures only.
"""

from __future__ import annotations


class KnowledgeError(Exception):
    """Base error for Knowledge Resolver."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class KnowledgeValidationError(KnowledgeError):
    """Knowledge contract validation failed."""
