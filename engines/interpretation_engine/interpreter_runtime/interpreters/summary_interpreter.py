"""Summary interpreter runtime skeleton. No BaZi logic."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpreterSkeletonRuntime,
)


class SummaryInterpreter(InterpreterSkeletonRuntime):
    """Summary interpreter skeleton — returns empty InterpretationSection."""

    interpreter_id = "summary_interpreter"
    section_type = "summary"
    version = "0.0.0-skeleton"
