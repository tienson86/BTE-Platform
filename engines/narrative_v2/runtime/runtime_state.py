"""Narrative V2 runtime state machine.

Transitions only. No narrative generation.
"""

from __future__ import annotations

from enum import Enum

from engines.narrative_v2.runtime.runtime_errors import PipelineError


class RuntimeState(Enum):
    """Canonical runtime lifecycle states (N-IMP-01)."""

    NOT_STARTED = "NOT_STARTED"
    INITIALIZED = "INITIALIZED"
    RUNNING = "RUNNING"
    VALIDATING = "VALIDATING"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"


ALLOWED_TRANSITIONS: dict[RuntimeState, frozenset[RuntimeState]] = {
    RuntimeState.NOT_STARTED: frozenset(
        {RuntimeState.INITIALIZED, RuntimeState.FAILED}
    ),
    RuntimeState.INITIALIZED: frozenset(
        {RuntimeState.RUNNING, RuntimeState.FAILED}
    ),
    RuntimeState.RUNNING: frozenset(
        {RuntimeState.VALIDATING, RuntimeState.FAILED}
    ),
    RuntimeState.VALIDATING: frozenset(
        {RuntimeState.PUBLISHED, RuntimeState.FAILED}
    ),
    RuntimeState.PUBLISHED: frozenset(),
    RuntimeState.FAILED: frozenset(),
}


def can_transition(current: RuntimeState, target: RuntimeState) -> bool:
    """Return True if ``current`` may move to ``target``."""
    return target in ALLOWED_TRANSITIONS[current]


def transition(current: RuntimeState, target: RuntimeState) -> RuntimeState:
    """Return ``target`` if the transition is legal.

    Raises:
        PipelineError: if the transition is not allowed.
    """
    if current is target:
        return current
    if not can_transition(current, target):
        raise PipelineError(
            f"Illegal state transition: {current.value} → {target.value}"
        )
    return target
