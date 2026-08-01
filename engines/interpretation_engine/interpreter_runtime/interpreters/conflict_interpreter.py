"""Conflict interpreter runtime skeleton. No BaZi logic."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpreterSkeletonRuntime,
)


class ConflictInterpreter(InterpreterSkeletonRuntime):
    """Conflict interpreter skeleton — returns empty InterpretationSection."""

    interpreter_id = "conflict_interpreter"
    section_type = "conflict"
    version = "0.0.0-skeleton"
