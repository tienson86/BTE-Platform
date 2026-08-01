"""Interpretation event type identifiers.

Local runtime event codes only. No external broker.
"""

from __future__ import annotations

from enum import Enum


class InterpretationEventType(str, Enum):
    """Internal event type codes for Pack 03 local Event Bus."""

    # Required runtime events
    BEFORE_INTERPRETER = "before_interpreter"
    AFTER_INTERPRETER = "after_interpreter"
    PIPELINE_STARTED = "pipeline_started"
    PIPELINE_FINISHED = "pipeline_finished"
    RUNTIME_ERROR = "runtime_error"
    HEALTH_CHANGED = "health_changed"

    # Retained compatibility codes
    PIPELINE_COMPLETED = "pipeline_completed"
    PIPELINE_FAILED = "pipeline_failed"
    INTERPRETER_STARTED = "interpreter_started"
    INTERPRETER_COMPLETED = "interpreter_completed"
    VALIDATION_FAILED = "validation_failed"


# Canonical required event set for audits/tests.
REQUIRED_RUNTIME_EVENTS: tuple[InterpretationEventType, ...] = (
    InterpretationEventType.BEFORE_INTERPRETER,
    InterpretationEventType.AFTER_INTERPRETER,
    InterpretationEventType.PIPELINE_STARTED,
    InterpretationEventType.PIPELINE_FINISHED,
    InterpretationEventType.RUNTIME_ERROR,
    InterpretationEventType.HEALTH_CHANGED,
)
