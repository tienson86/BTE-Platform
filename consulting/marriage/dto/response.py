"""Runtime and API response DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field

from consulting.marriage.dto.presentation import MarriagePresentationResult
from consulting.marriage.models.enums import MarriageRuntimeStatus
from consulting.marriage.models.result import MarriageDecisionResult


@dataclass(slots=True)
class RuntimeWarning:
    """Non-fatal runtime warning. Customer text is not taken from technical_detail."""

    code: str
    stage: str
    message_key: str | None = None
    technical_detail: str | None = None
    affected_domain: str | None = None


@dataclass(slots=True)
class RuntimeError:
    """Runtime error envelope. Stack traces are not exposed."""

    code: str
    stage: str
    retryable: bool
    technical_detail: str | None = None


@dataclass(slots=True)
class StageTiming:
    """Internal stage duration. Not a customer field."""

    stage: str
    duration_ms: float


@dataclass(slots=True)
class MarriageRuntimeResponse:
    """Internal runtime envelope. Not the public API resource."""

    status: MarriageRuntimeStatus
    consultation_id: str | None = None
    result: MarriageDecisionResult | None = None
    presentation: MarriagePresentationResult | None = None
    warnings: list[RuntimeWarning] = field(default_factory=list)
    error: RuntimeError | None = None


@dataclass(slots=True)
class MarriageConsultationSummary:
    """Compact consultation summary resource."""

    consultation_id: str
    person_a_analysis_id: str
    person_b_analysis_id: str
    score: float
    grade: str
    confidence: float
