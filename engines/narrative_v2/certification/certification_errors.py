"""Certification errors. Decision records only — no Narrative writes."""

from __future__ import annotations


class CertificationError(Exception):
    """Base error for the Narrative Certification Gate."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class CertificationTransitionError(CertificationError):
    """Illegal certification state transition."""


class CertificationRejectedError(CertificationError):
    """CERTIFIED was requested but quality gates or reviewer rules failed."""
