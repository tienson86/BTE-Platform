"""Season interpreter runtime skeleton. No BaZi logic."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpreterSkeletonRuntime,
)


class SeasonInterpreter(InterpreterSkeletonRuntime):
    """Season interpreter skeleton — returns empty InterpretationSection."""

    interpreter_id = "season_interpreter"
    section_type = "season"
    version = "0.0.0-skeleton"
