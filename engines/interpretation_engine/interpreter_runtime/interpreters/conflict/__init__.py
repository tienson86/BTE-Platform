"""Conflict Interpreter package — Pack 03 conflict business logic module."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.constants import (
    CONFLICT_INTERPRETER_ID,
    CONFLICT_INTERPRETER_VERSION,
    CONFLICT_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.models import (
    ConflictComponentResult,
    ConflictInterpretationSection,
    ConflictItemResult,
)

__all__ = [
    "CONFLICT_INTERPRETER_ID",
    "CONFLICT_INTERPRETER_VERSION",
    "CONFLICT_SECTION_TYPE",
    "ConflictComponentResult",
    "ConflictFactExtractor",
    "ConflictFacts",
    "ConflictInterpretationRuleEngine",
    "ConflictInterpretationSection",
    "ConflictInterpreterService",
    "ConflictItemResult",
    "ConflictRuleEngineResult",
    "ConflictRuleLoader",
]


def __getattr__(name: str):
    """Lazy export heavy modules to avoid import cycles."""
    if name in {"ConflictFactExtractor", "ConflictFacts"}:
        from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.extractor import (
            ConflictFactExtractor,
            ConflictFacts,
        )

        return ConflictFactExtractor if name == "ConflictFactExtractor" else ConflictFacts
    if name in {"ConflictInterpretationRuleEngine", "ConflictRuleEngineResult"}:
        from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.rule_engine import (
            ConflictInterpretationRuleEngine,
            ConflictRuleEngineResult,
        )

        return (
            ConflictInterpretationRuleEngine
            if name == "ConflictInterpretationRuleEngine"
            else ConflictRuleEngineResult
        )
    if name == "ConflictRuleLoader":
        from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.rule_loader import (
            ConflictRuleLoader,
        )

        return ConflictRuleLoader
    if name == "ConflictInterpreterService":
        from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.service import (
            ConflictInterpreterService,
        )

        return ConflictInterpreterService
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
