"""Certification result and allowed states."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

STATUS_DRAFT = "DRAFT"
STATUS_REVIEW = "REVIEW"
STATUS_CERTIFIED = "CERTIFIED"
STATUS_REJECTED = "REJECTED"
STATUS_REVOKED = "REVOKED"

ALLOWED_STATES: frozenset[str] = frozenset(
    {
        STATUS_DRAFT,
        STATUS_REVIEW,
        STATUS_CERTIFIED,
        STATUS_REJECTED,
        STATUS_REVOKED,
    }
)

DECISIONS: frozenset[str] = frozenset(
    {
        STATUS_REVIEW,
        STATUS_CERTIFIED,
        STATUS_REJECTED,
        STATUS_REVOKED,
    }
)

CERTIFICATION_VERSION = "bte.certification.v1"

QUALITY_GATES: tuple[str, ...] = (
    "technical",
    "semantic",
    "language",
    "conversation",
    "consulting",
    "presentation",
    "export",
    "no_critical_issues",
)


@dataclass(frozen=True, slots=True)
class CertificationResult:
    """One append-only certification decision. Does not mutate Narrative."""

    review_id: str
    case_id: str
    status: str
    decision: str
    reviewer: str
    review_time: str
    review_comment: str
    quality_summary: Mapping[str, Any]
    certification_version: str
    references: Mapping[str, Any]
    metadata: Mapping[str, Any]
    golden_eligible: bool

    def to_record(self) -> dict[str, Any]:
        """Serialize a history row."""
        return {
            "review_id": self.review_id,
            "case_id": self.case_id,
            "status": self.status,
            "decision": self.decision,
            "reviewer": self.reviewer,
            "review_time": self.review_time,
            "review_comment": self.review_comment,
            "quality_summary": dict(self.quality_summary),
            "certification_version": self.certification_version,
            "references": dict(self.references),
            "metadata": dict(self.metadata),
            "golden_eligible": self.golden_eligible,
        }
