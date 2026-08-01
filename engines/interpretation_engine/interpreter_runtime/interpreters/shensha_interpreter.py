"""Shensha interpreter runtime skeleton. No BaZi logic."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpreterSkeletonRuntime,
)


class ShenshaInterpreter(InterpreterSkeletonRuntime):
    """Shensha interpreter skeleton — returns empty InterpretationSection."""

    interpreter_id = "shensha_interpreter"
    section_type = "shensha"
    version = "0.0.0-skeleton"
