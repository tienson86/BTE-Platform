"""TV-01 Marriage DTO package."""

from __future__ import annotations

from consulting.marriage.dto.history import MarriageHistoryRecord, MarriageStoredResult
from consulting.marriage.dto.presentation import (
    MarriageConfidenceView,
    MarriageDomainView,
    MarriageFindingView,
    MarriageHeroView,
    MarriageIdentityView,
    MarriagePresentationResult,
    MarriageRecommendationView,
    MarriageTimingView,
)
from consulting.marriage.dto.request import (
    BirthPlaceInput,
    CanonicalBirthInput,
    MarriageConsultationOptions,
    MarriageConsultationRequest,
    MarriagePersonInput,
    NormalizedMarriageRequest,
    RequestMeta,
)
from consulting.marriage.models.options import ResolvedMarriageOptions
from consulting.marriage.dto.response import (
    MarriageConsultationSummary,
    MarriageRuntimeResponse,
    RuntimeError,
    RuntimeWarning,
    StageTiming,
)

__all__ = [
    "BirthPlaceInput",
    "CanonicalBirthInput",
    "MarriageConfidenceView",
    "MarriageConsultationOptions",
    "MarriageConsultationRequest",
    "MarriageConsultationSummary",
    "MarriageDomainView",
    "MarriageFindingView",
    "MarriageHeroView",
    "MarriageHistoryRecord",
    "MarriageIdentityView",
    "MarriagePersonInput",
    "MarriagePresentationResult",
    "MarriageRecommendationView",
    "MarriageRuntimeResponse",
    "MarriageStoredResult",
    "MarriageTimingView",
    "NormalizedMarriageRequest",
    "RequestMeta",
    "ResolvedMarriageOptions",
    "RuntimeError",
    "RuntimeWarning",
    "StageTiming",
]
