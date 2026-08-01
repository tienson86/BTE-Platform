"""Interpretation event type identifiers."""

from __future__ import annotations

from enum import Enum


class InterpretationEventType(str, Enum):
    """Internal event type codes for Pack 03."""

    PIPELINE_STARTED = "pipeline_started"
    PIPELINE_COMPLETED = "pipeline_completed"
    PIPELINE_FAILED = "pipeline_failed"
    INTERPRETER_STARTED = "interpreter_started"
    INTERPRETER_COMPLETED = "interpreter_completed"
    VALIDATION_FAILED = "validation_failed"
