"""Certification input context. Presentation and review metadata only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class CertificationContext:
    """Inputs the gate may read. No CanonicalAnalysis. No Pack05."""

    case_id: str
    presentation: Mapping[str, Any]
    studio_review: Mapping[str, Any]
    validation_summary: Mapping[str, Any]
    test_summary: Mapping[str, Any]
    reviewer: str
    review_comment: str
    review_time: str | None = None
