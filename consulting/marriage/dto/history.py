"""History DTOs. Persistence shapes only."""

from __future__ import annotations

from dataclasses import dataclass

from consulting.marriage.dto.presentation import MarriagePresentationResult
from consulting.marriage.dto.request import MarriageConsultationRequest
from consulting.marriage.models.enums import DomainGrade
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.models.versioning import MarriageVersionBundle


@dataclass(slots=True)
class MarriageHistoryRecord:
    """Compact history row. Does not embed the full decision."""

    consultation_id: str
    person_a_analysis_id: str
    person_b_analysis_id: str
    score: float
    grade: DomainGrade
    confidence: float
    versions: MarriageVersionBundle
    created_at: str
    display_label: str | None = None


@dataclass(slots=True)
class MarriageStoredResult:
    """Full stored consultation payload."""

    history: MarriageHistoryRecord
    request: MarriageConsultationRequest
    result: MarriageDecisionResult
    presentation: MarriagePresentationResult | None = None
