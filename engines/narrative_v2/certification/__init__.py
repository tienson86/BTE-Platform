"""Narrative Certification Gate — final approval before Golden Dataset.

Records decisions only. Does not modify Narrative, Knowledge, or Presentation.
"""

from __future__ import annotations

from engines.narrative_v2.certification.certification_context import CertificationContext
from engines.narrative_v2.certification.certification_errors import (
    CertificationError,
    CertificationRejectedError,
    CertificationTransitionError,
)
from engines.narrative_v2.certification.certification_gate import CertificationGate
from engines.narrative_v2.certification.certification_history import CertificationHistory
from engines.narrative_v2.certification.certification_registry import (
    ALLOWED_TRANSITIONS,
    can_transition,
)
from engines.narrative_v2.certification.certification_result import (
    ALLOWED_STATES,
    CERTIFICATION_VERSION,
    DECISIONS,
    QUALITY_GATES,
    STATUS_CERTIFIED,
    STATUS_DRAFT,
    STATUS_REJECTED,
    STATUS_REVIEW,
    STATUS_REVOKED,
    CertificationResult,
)
from engines.narrative_v2.certification.certification_validator import CertificationValidator

__all__ = [
    "ALLOWED_STATES",
    "ALLOWED_TRANSITIONS",
    "CERTIFICATION_VERSION",
    "DECISIONS",
    "QUALITY_GATES",
    "STATUS_CERTIFIED",
    "STATUS_DRAFT",
    "STATUS_REJECTED",
    "STATUS_REVIEW",
    "STATUS_REVOKED",
    "CertificationContext",
    "CertificationError",
    "CertificationGate",
    "CertificationHistory",
    "CertificationRejectedError",
    "CertificationResult",
    "CertificationTransitionError",
    "CertificationValidator",
    "can_transition",
]
