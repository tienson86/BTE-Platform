"""TV-01 runtime lifecycle states. B02 stops at SNAPSHOT_READY → COMPLETED."""

from __future__ import annotations

from enum import Enum


class RuntimeLifecycleState(str, Enum):
    """Allowed runtime states through decision completion. No report/UI states."""

    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    CANONICAL_READY = "CANONICAL_READY"
    SNAPSHOT_READY = "SNAPSHOT_READY"
    EVIDENCE_READY = "EVIDENCE_READY"
    DECISION_READY = "DECISION_READY"
    RECOMMENDATION_READY = "RECOMMENDATION_READY"
    COMPLETED = "COMPLETED"


LIFECYCLE_ORDER: tuple[RuntimeLifecycleState, ...] = (
    RuntimeLifecycleState.CREATED,
    RuntimeLifecycleState.VALIDATED,
    RuntimeLifecycleState.CANONICAL_READY,
    RuntimeLifecycleState.SNAPSHOT_READY,
    RuntimeLifecycleState.EVIDENCE_READY,
    RuntimeLifecycleState.DECISION_READY,
    RuntimeLifecycleState.RECOMMENDATION_READY,
    RuntimeLifecycleState.COMPLETED,
)
