"""Allowed certification state transitions."""

from __future__ import annotations

from engines.narrative_v2.certification.certification_result import (
    STATUS_CERTIFIED,
    STATUS_DRAFT,
    STATUS_REJECTED,
    STATUS_REVIEW,
    STATUS_REVOKED,
)

ALLOWED_TRANSITIONS: dict[str, frozenset[str]] = {
    STATUS_DRAFT: frozenset({STATUS_REVIEW, STATUS_REJECTED}),
    STATUS_REVIEW: frozenset({STATUS_CERTIFIED, STATUS_REJECTED, STATUS_REVIEW}),
    STATUS_CERTIFIED: frozenset({STATUS_REVOKED}),
    STATUS_REJECTED: frozenset({STATUS_REVIEW}),
    STATUS_REVOKED: frozenset({STATUS_REVIEW}),
}


def can_transition(current: str, decision: str) -> bool:
    """True when decision is a legal next status."""
    allowed = ALLOWED_TRANSITIONS.get(current, frozenset())
    return decision in allowed
