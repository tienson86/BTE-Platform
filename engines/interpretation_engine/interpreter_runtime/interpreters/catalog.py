"""Catalog of Pack 03 interpreter runtime skeletons.

Dependency injection helpers only. No singleton globals. No BaZi logic.
"""

from __future__ import annotations

from typing import Sequence

from engines.interpretation_engine.interpreter_runtime.dispatcher import (
    InterpreterDispatcher,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpreterSkeletonRuntime,
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
from engines.interpretation_engine.interpreter_runtime.registry import (
    InterpreterRuntimeRegistry,
)

INTERPRETER_SKELETON_CLASSES: tuple[type[InterpreterSkeletonRuntime], ...] = (
    StrengthInterpreter,
    SeasonInterpreter,
    TemperatureInterpreter,
    PatternInterpreter,
    UsefulGodInterpreter,
    CombinationInterpreter,
    ConflictInterpreter,
    TenGodsInterpreter,
    ShenshaInterpreter,
    LuckInterpreter,
    ScoringInterpreter,
    SummaryInterpreter,
)

INTERPRETER_SKELETON_IDS: tuple[str, ...] = tuple(
    cls.interpreter_id for cls in INTERPRETER_SKELETON_CLASSES
)

# Default execution priorities (lower runs first). Structural ordering only.
_DEFAULT_PRIORITIES: dict[str, int] = {
    "strength_interpreter": 10,
    "season_interpreter": 20,
    "temperature_interpreter": 30,
    "pattern_interpreter": 40,
    "useful_god_interpreter": 50,
    "combination_interpreter": 60,
    "conflict_interpreter": 70,
    "ten_gods_interpreter": 80,
    "shensha_interpreter": 90,
    "luck_interpreter": 100,
    "scoring_interpreter": 110,
    "summary_interpreter": 120,
}


def create_all_interpreter_skeletons() -> tuple[InterpreterSkeletonRuntime, ...]:
    """Instantiate all interpreter skeleton runtimes (DI factory)."""
    return tuple(cls() for cls in INTERPRETER_SKELETON_CLASSES)


def register_interpreter_skeletons(
    *,
    registry: InterpreterRuntimeRegistry | None = None,
    dispatcher: InterpreterDispatcher | None = None,
    skeletons: Sequence[InterpreterSkeletonRuntime] | None = None,
) -> tuple[InterpreterSkeletonRuntime, ...]:
    """Register skeleton instances into optional registry and dispatcher.

    Handlers execute the skeleton ``execute`` method and return its result.
    """
    instances = tuple(skeletons) if skeletons is not None else create_all_interpreter_skeletons()
    for index, skeleton in enumerate(instances):
        if registry is not None:
            registry.register(
                skeleton.interpreter_id,
                {
                    "interpreter_id": skeleton.interpreter_id,
                    "section_type": skeleton.section_type,
                    "version": skeleton.version,
                    "skeleton": True,
                },
            )
        if dispatcher is not None:
            priority = _DEFAULT_PRIORITIES.get(skeleton.interpreter_id, 100 + index)

            def _handler(
                context: object,
                *,
                _runtime: InterpreterSkeletonRuntime = skeleton,
            ) -> object:
                return _runtime.execute(context)

            dispatcher.register(
                skeleton.interpreter_id,
                _handler,
                priority=priority,
                metadata={"section_type": skeleton.section_type},
            )
    return instances
