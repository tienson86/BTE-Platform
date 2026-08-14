"""Knowledge status lifecycle for interpretation knowledge entities."""

from __future__ import annotations

from enum import Enum


class KnowledgeStatus(str, Enum):
    """Entity publication status."""

    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    DEPRECATED = "deprecated"
