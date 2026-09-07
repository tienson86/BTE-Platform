"""TV-01 Marriage Consulting exception types.

Typed errors only. No fallback or suppression logic.
"""

from __future__ import annotations


class MarriageConsultingError(Exception):
    """Base exception for TV-01 Marriage Consulting."""


class MarriageValidationError(MarriageConsultingError):
    """Request or business-contract validation failed."""


class MarriageCanonicalAnalysisError(MarriageConsultingError):
    """Canonical analysis for Person A or Person B failed."""


class MarriageCanonicalContractError(MarriageConsultingError):
    """Canonical result did not match the expected contract."""


class MarriageEvidenceError(MarriageConsultingError):
    """Evidence construction or validation failed."""


class MarriageDecisionError(MarriageConsultingError):
    """Decision construction or validation failed."""


class MarriageScoreError(MarriageConsultingError):
    """Score projection failed."""


class MarriageConfidenceError(MarriageConsultingError):
    """Confidence construction failed."""


class MarriageNarrativeError(MarriageConsultingError):
    """Narrative composition failed."""


class MarriagePersistenceError(MarriageConsultingError):
    """Persistence of a consultation result failed."""


class MarriageNotFoundError(MarriageConsultingError):
    """Requested consultation resource does not exist."""


class MarriageConflictError(MarriageConsultingError):
    """Idempotency key conflicts with a different stored request."""


class MarriageInternalError(MarriageConsultingError):
    """Unexpected internal failure."""


class MarriageRecommendationError(MarriageConsultingError):
    """Recommendation construction or validation failed."""
