"""Useful god interpreter runtime skeleton. No BaZi logic."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpreterSkeletonRuntime,
)


class UsefulGodInterpreter(InterpreterSkeletonRuntime):
    """Useful god interpreter skeleton — returns empty InterpretationSection."""

    interpreter_id = "useful_god_interpreter"
    section_type = "useful_god"
    version = "0.0.0-skeleton"
