"""Backward-compatible re-export of repository interfaces (WP11)."""

from applications.storage.interfaces.repository import (
    DocumentRepository,
    Repository,
)

__all__ = ["DocumentRepository", "Repository"]
