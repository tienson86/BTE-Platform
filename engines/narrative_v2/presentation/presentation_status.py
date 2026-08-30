"""Presentation statuses and versions."""

from __future__ import annotations

STATUS_COMPLETE = "complete"
STATUS_PARTIAL = "partial"
STATUS_INSUFFICIENT = "insufficient"
STATUS_INVALID = "invalid"

ALLOWED_STATUSES: frozenset[str] = frozenset(
    {
        STATUS_COMPLETE,
        STATUS_PARTIAL,
        STATUS_INSUFFICIENT,
        STATUS_INVALID,
    }
)

PRESENTATION_VERSION = "bte.presentation.v2"
NARRATIVE_VERSION = "bte.narrative.v2"
DEFAULT_LANGUAGE = "vi"
FROZEN_CREATED_AT = "1970-01-01T00:00:00Z"
