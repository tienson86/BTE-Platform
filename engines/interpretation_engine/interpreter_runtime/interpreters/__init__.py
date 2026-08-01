"""Interpreter runtime skeleton implementations.

Infrastructure only. No BaZi rules, calculations, or narrative content.
Each skeleton returns an empty InterpretationSection (SectionResult shell).
"""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpreterSkeletonRuntime,
    empty_interpretation_section,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.catalog import (
    INTERPRETER_SKELETON_CLASSES,
    INTERPRETER_SKELETON_IDS,
    create_all_interpreter_skeletons,
    register_interpreter_skeletons,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.combination_interpreter import (
    CombinationInterpreter,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.conflict_interpreter import (
    ConflictInterpreter,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.luck_interpreter import (
    LuckInterpreter,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.pattern_interpreter import (
    PatternInterpreter,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.scoring_interpreter import (
    ScoringInterpreter,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.season_interpreter import (
    SeasonInterpreter,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.shensha_interpreter import (
    ShenshaInterpreter,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.strength_interpreter import (
    StrengthInterpreter,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.summary_interpreter import (
    SummaryInterpreter,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.temperature_interpreter import (
    TemperatureInterpreter,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods_interpreter import (
    TenGodsInterpreter,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.useful_god_interpreter import (
    UsefulGodInterpreter,
)
from engines.interpretation_engine.models.section_result import SectionResult

# Canonical empty section type for interpreter skeletons.
InterpretationSection = SectionResult

__all__ = [
    "INTERPRETER_SKELETON_CLASSES",
    "INTERPRETER_SKELETON_IDS",
    "CombinationInterpreter",
    "ConflictInterpreter",
    "InterpretationSection",
    "InterpreterSkeletonRuntime",
    "LuckInterpreter",
    "PatternInterpreter",
    "ScoringInterpreter",
    "SeasonInterpreter",
    "ShenshaInterpreter",
    "StrengthInterpreter",
    "SummaryInterpreter",
    "TemperatureInterpreter",
    "TenGodsInterpreter",
    "UsefulGodInterpreter",
    "create_all_interpreter_skeletons",
    "empty_interpretation_section",
    "register_interpreter_skeletons",
]
