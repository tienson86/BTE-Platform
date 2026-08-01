"""Pattern interpreter runtime skeleton. No BaZi logic."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpreterSkeletonRuntime,
)


class PatternInterpreter(InterpreterSkeletonRuntime):
    """Pattern interpreter skeleton — returns empty InterpretationSection."""

    interpreter_id = "pattern_interpreter"
    section_type = "pattern"
    version = "0.0.0-skeleton"
