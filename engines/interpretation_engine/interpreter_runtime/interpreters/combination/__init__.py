"""Combination Interpreter package — Pack 03 combination business logic module."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.combination.constants import (
    COMBINATION_INTERPRETER_ID,
    COMBINATION_INTERPRETER_VERSION,
    COMBINATION_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.combination.models import (
    CombinationComponentResult,
    CombinationInterpretationSection,
    CombinationItemResult,
)

__all__ = [
    "COMBINATION_INTERPRETER_ID",
    "COMBINATION_INTERPRETER_VERSION",
    "COMBINATION_SECTION_TYPE",
    "CombinationComponentResult",
    "CombinationFactExtractor",
    "CombinationFacts",
    "CombinationInterpretationRuleEngine",
    "CombinationInterpretationSection",
    "CombinationInterpreterService",
    "CombinationItemResult",
    "CombinationRuleEngineResult",
    "CombinationRuleLoader",
]


def __getattr__(name: str):
    """Lazy export heavy modules to avoid import cycles."""
    if name in {"CombinationFactExtractor", "CombinationFacts"}:
        from engines.interpretation_engine.interpreter_runtime.interpreters.combination.extractor import (
            CombinationFactExtractor,
            CombinationFacts,
        )

        return CombinationFactExtractor if name == "CombinationFactExtractor" else CombinationFacts
    if name in {"CombinationInterpretationRuleEngine", "CombinationRuleEngineResult"}:
        from engines.interpretation_engine.interpreter_runtime.interpreters.combination.rule_engine import (
            CombinationInterpretationRuleEngine,
            CombinationRuleEngineResult,
        )

        return (
            CombinationInterpretationRuleEngine
            if name == "CombinationInterpretationRuleEngine"
            else CombinationRuleEngineResult
        )
    if name == "CombinationRuleLoader":
        from engines.interpretation_engine.interpreter_runtime.interpreters.combination.rule_loader import (
            CombinationRuleLoader,
        )

        return CombinationRuleLoader
    if name == "CombinationInterpreterService":
        from engines.interpretation_engine.interpreter_runtime.interpreters.combination.service import (
            CombinationInterpreterService,
        )

        return CombinationInterpreterService
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
