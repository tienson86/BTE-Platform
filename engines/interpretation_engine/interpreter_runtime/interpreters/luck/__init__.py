"""Luck Interpreter package — Pack 03 luck business logic module."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.luck.constants import (
    LUCK_INTERPRETER_ID,
    LUCK_INTERPRETER_VERSION,
    LUCK_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.luck.models import (
    LuckComponentResult,
    LuckInterpretationSection,
    LuckItemResult,
)

__all__ = [
    "LUCK_INTERPRETER_ID",
    "LUCK_INTERPRETER_VERSION",
    "LUCK_SECTION_TYPE",
    "LuckComponentResult",
    "LuckFactExtractor",
    "LuckFacts",
    "LuckInterpretationRuleEngine",
    "LuckInterpretationSection",
    "LuckInterpreterService",
    "LuckItemResult",
    "LuckRuleEngineResult",
    "LuckRuleLoader",
]


def __getattr__(name: str):
    """Lazy export heavy modules to avoid import cycles."""
    if name in {"LuckFactExtractor", "LuckFacts"}:
        from engines.interpretation_engine.interpreter_runtime.interpreters.luck.extractor import (
            LuckFactExtractor,
            LuckFacts,
        )

        return LuckFactExtractor if name == "LuckFactExtractor" else LuckFacts
    if name in {"LuckInterpretationRuleEngine", "LuckRuleEngineResult"}:
        from engines.interpretation_engine.interpreter_runtime.interpreters.luck.rule_engine import (
            LuckInterpretationRuleEngine,
            LuckRuleEngineResult,
        )

        return (
            LuckInterpretationRuleEngine
            if name == "LuckInterpretationRuleEngine"
            else LuckRuleEngineResult
        )
    if name == "LuckRuleLoader":
        from engines.interpretation_engine.interpreter_runtime.interpreters.luck.rule_loader import (
            LuckRuleLoader,
        )

        return LuckRuleLoader
    if name == "LuckInterpreterService":
        from engines.interpretation_engine.interpreter_runtime.interpreters.luck.service import (
            LuckInterpreterService,
        )

        return LuckInterpreterService
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
