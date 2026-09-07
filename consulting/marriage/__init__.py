"""TV-01 Marriage Consulting public package.

Skeleton only for TV1-B01. No business logic. No Canonical or COMMON edits.
"""

from __future__ import annotations

from consulting.marriage.constants import BUILD_PHASE, MODULE_ID, MODULE_VERSION, PIPELINE_STAGES
from consulting.marriage.contracts import (
    CanonicalRuntimeAdapter,
    MarriageApiContract,
    MarriageDecisionContext,
    MarriageOrchestrator,
    MarriagePolicyProvider,
    MarriageRecommendationProvider,
    MarriageReportProfile,
    MarriageRepository,
    MarriageRuntimeContext,
    MarriageUILayoutProfile,
    MarriageValidationContract,
)
from consulting.marriage.exceptions import MarriageConsultingError
from consulting.marriage.runtime.container import MarriageContainer
from consulting.marriage.runtime.wiring import wire_marriage_runtime

__all__ = [
    "BUILD_PHASE",
    "MODULE_ID",
    "MODULE_VERSION",
    "PIPELINE_STAGES",
    "CanonicalRuntimeAdapter",
    "MarriageApiContract",
    "MarriageConsultingError",
    "MarriageContainer",
    "MarriageDecisionContext",
    "MarriageOrchestrator",
    "MarriagePolicyProvider",
    "MarriageRecommendationProvider",
    "MarriageReportProfile",
    "MarriageRepository",
    "MarriageRuntimeContext",
    "MarriageUILayoutProfile",
    "MarriageValidationContract",
    "wire_marriage_runtime",
]
