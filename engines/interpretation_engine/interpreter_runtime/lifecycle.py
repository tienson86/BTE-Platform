"""Interpreter runtime lifecycle helpers."""

from __future__ import annotations

from enum import Enum


class InterpreterLifecyclePhase(str, Enum):
    """Lifecycle phases for interpreter runtime orchestration."""

    CREATED = "created"
    INITIALIZED = "initialized"
    DISPATCHING = "dispatching"
    COMPLETED = "completed"
    FAILED = "failed"
    SHUTDOWN = "shutdown"
