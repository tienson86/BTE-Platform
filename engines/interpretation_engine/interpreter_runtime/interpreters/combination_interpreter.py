"""Combination interpreter runtime skeleton. No BaZi logic."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpreterSkeletonRuntime,
)


class CombinationInterpreter(InterpreterSkeletonRuntime):
    """Combination interpreter skeleton — returns empty InterpretationSection."""

    interpreter_id = "combination_interpreter"
    section_type = "combination"
    version = "0.0.0-skeleton"
