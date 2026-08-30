"""Release monitoring errors."""

from __future__ import annotations


class ReleaseError(Exception):
    """Release monitoring failure."""


class ReleaseHistoryError(ReleaseError):
    """Append-only history was mutated or invalid."""
