"""Availability and readiness vocabulary for Interpretation Foundation."""

from __future__ import annotations

from enum import Enum


class DataAvailability(str, Enum):
    """Explicit analytical data availability — never use None/0/-- as status."""

    AVAILABLE = "available"
    PARTIAL = "partial"
    MISSING = "missing"
    NOT_IMPLEMENTED = "not_implemented"
    INVALID = "invalid"
    FALLBACK = "fallback"


class ReadinessLevel(str, Enum):
    """Domain interpretation readiness (data only, not prose quality)."""

    READY = "ready"
    PARTIAL = "partial"
    MISSING = "missing"
    NOT_READY = "not_ready"


class EvidenceStatus(str, Enum):
    """Evidence availability for structured facts."""

    AVAILABLE = "available"
    PARTIAL = "partial"
    UNAVAILABLE = "unavailable"
