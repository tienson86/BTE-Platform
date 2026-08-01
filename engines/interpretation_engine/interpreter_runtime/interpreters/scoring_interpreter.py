"""Scoring interpreter runtime skeleton. No BaZi logic."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpreterSkeletonRuntime,
)


class ScoringInterpreter(InterpreterSkeletonRuntime):
    """Scoring interpreter skeleton — returns empty InterpretationSection."""

    interpreter_id = "scoring_interpreter"
    section_type = "scoring"
    version = "0.0.0-skeleton"
