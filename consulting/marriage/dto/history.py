"""History DTOs. Persistence shapes only."""

from __future__ import annotations

from dataclasses import dataclass, field

from consulting.marriage.dto.presentation import MarriagePresentationResult
from consulting.marriage.dto.request import MarriageConsultationRequest
from consulting.marriage.dto.response import RuntimeWarning
from consulting.marriage.models.enums import DomainGrade, MarriageRuntimeStatus
from consulting.marriage.models.narrative import MarriageNarrativeResult
from consulting.marriage.models.report import MarriageReportModel
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.models.versioning import MarriageVersionBundle


@dataclass(slots=True)
class MarriageHistoryRecord:
    """Compact history row. Does not embed the full decision or rendered prose."""

    consultation_id: str
    person_a_analysis_id: str
    person_b_analysis_id: str
    score: float | None
    grade: DomainGrade | None
    confidence: float
    versions: MarriageVersionBundle
    created_at: str
    display_label: str | None = None
    status: str | None = None
    overall_state: str | None = None
    language: str | None = None


@dataclass(slots=True)
class MarriageStoredResult:
    """Full stored consultation payload."""

    history: MarriageHistoryRecord
    request: MarriageConsultationRequest
    result: MarriageDecisionResult
    presentation: MarriagePresentationResult | None = None
    narrative: MarriageNarrativeResult | None = None
    report_model: MarriageReportModel | None = None
    warnings: list[RuntimeWarning] = field(default_factory=list)
    status: MarriageRuntimeStatus = MarriageRuntimeStatus.SUCCESS
    idempotency_key: str | None = None
    request_fingerprint: str | None = None
