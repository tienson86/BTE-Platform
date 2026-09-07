"""TV-01 B02 runtime lifecycle states. No Decision states."""

from __future__ import annotations

from enum import Enum


class RuntimeLifecycleState(str, Enum):
    """Allowed runtime states through snapshot completion."""

    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    CANONICAL_READY = "CANONICAL_READY"
    SNAPSHOT_READY = "SNAPSHOT_READY"
    COMPLETED = "COMPLETED"


LIFECYCLE_ORDER: tuple[RuntimeLifecycleState, ...] = (
    RuntimeLifecycleState.CREATED,
    RuntimeLifecycleState.VALIDATED,
    RuntimeLifecycleState.CANONICAL_READY,
    RuntimeLifecycleState.SNAPSHOT_READY,
    RuntimeLifecycleState.COMPLETED,
)
