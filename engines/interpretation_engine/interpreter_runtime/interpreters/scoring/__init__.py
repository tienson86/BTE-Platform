"""Scoring Interpreter package — Pack 03 scoring business logic module."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.scoring.constants import (
    SCORING_INTERPRETER_ID,
    SCORING_INTERPRETER_VERSION,
    SCORING_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.scoring.models import (
    ScoringComponentResult,
    ScoringInterpretationSection,
    ScoringItemResult,
)

__all__ = [
    "SCORING_INTERPRETER_ID",
    "SCORING_INTERPRETER_VERSION",
    "SCORING_SECTION_TYPE",
    "ScoringComponentResult",
    "ScoringFactExtractor",
    "ScoringFacts",
    "ScoringInterpretationRuleEngine",
    "ScoringInterpretationSection",
    "ScoringInterpreterService",
    "ScoringItemResult",
    "ScoringRuleEngineResult",
    "ScoringRuleLoader",
]


def __getattr__(name: str):
    """Lazy export heavy modules to avoid import cycles."""
    if name in {"ScoringFactExtractor", "ScoringFacts"}:
        from engines.interpretation_engine.interpreter_runtime.interpreters.scoring.extractor import (
            ScoringFactExtractor,
            ScoringFacts,
        )

        return ScoringFactExtractor if name == "ScoringFactExtractor" else ScoringFacts
    if name in {"ScoringInterpretationRuleEngine", "ScoringRuleEngineResult"}:
        from engines.interpretation_engine.interpreter_runtime.interpreters.scoring.rule_engine import (
            ScoringInterpretationRuleEngine,
            ScoringRuleEngineResult,
        )

        return (
            ScoringInterpretationRuleEngine
            if name == "ScoringInterpretationRuleEngine"
            else ScoringRuleEngineResult
        )
    if name == "ScoringRuleLoader":
        from engines.interpretation_engine.interpreter_runtime.interpreters.scoring.rule_loader import (
            ScoringRuleLoader,
        )

        return ScoringRuleLoader
    if name == "ScoringInterpreterService":
        from engines.interpretation_engine.interpreter_runtime.interpreters.scoring.service import (
            ScoringInterpreterService,
        )

        return ScoringInterpreterService
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
