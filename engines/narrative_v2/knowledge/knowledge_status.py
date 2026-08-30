"""Approval status tokens for Narrative V2 knowledge resolution."""

from __future__ import annotations

STATUS_APPROVED = "approved"
STATUS_DRAFT = "draft"
STATUS_REVIEW = "review"
STATUS_DEPRECATED = "deprecated"

ELIGIBLE_SOURCE_STATUSES: frozenset[str] = frozenset({STATUS_APPROVED})

RESOLVED = "resolved"
UNRESOLVED = "unresolved"
PARTIAL = "partial"

REASON_NO_APPROVED_KNOWLEDGE = "no_approved_knowledge"
REASON_UNSUPPORTED_SEMANTIC_KEY = "unsupported_semantic_key"
REASON_AMBIGUOUS_ALIAS = "ambiguous_alias"
REASON_SOURCE_NOT_APPROVED = "source_not_approved"
REASON_VERSION_MISMATCH = "version_mismatch"

ALLOWED_KNOWLEDGE_TYPES: frozenset[str] = frozenset(
    {
        "meaning",
        "boundary",
        "recommendation",
        "warning",
        "domain_context",
        "terminology",
        "supporting_explanation",
    }
)

RESOLVER_VERSION = "nimp04.1.0"
