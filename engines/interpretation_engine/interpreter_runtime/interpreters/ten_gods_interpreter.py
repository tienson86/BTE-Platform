"""Ten gods interpreter runtime skeleton. No BaZi logic."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpreterSkeletonRuntime,
)


class TenGodsInterpreter(InterpreterSkeletonRuntime):
    """Ten gods interpreter skeleton — returns empty InterpretationSection."""

    interpreter_id = "ten_gods_interpreter"
    section_type = "ten_gods"
    version = "0.0.0-skeleton"
