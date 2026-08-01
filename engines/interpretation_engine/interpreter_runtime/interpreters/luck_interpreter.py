"""Luck interpreter runtime skeleton. No BaZi logic."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpreterSkeletonRuntime,
)


class LuckInterpreter(InterpreterSkeletonRuntime):
    """Luck interpreter skeleton — returns empty InterpretationSection."""

    interpreter_id = "luck_interpreter"
    section_type = "luck"
    version = "0.0.0-skeleton"
