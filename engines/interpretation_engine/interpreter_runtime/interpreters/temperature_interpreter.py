"""Temperature interpreter runtime skeleton. No BaZi logic."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpreterSkeletonRuntime,
)


class TemperatureInterpreter(InterpreterSkeletonRuntime):
    """Temperature interpreter skeleton — returns empty InterpretationSection."""

    interpreter_id = "temperature_interpreter"
    section_type = "temperature"
    version = "0.0.0-skeleton"
