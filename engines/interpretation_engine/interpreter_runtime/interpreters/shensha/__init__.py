"""Shensha Interpreter package — Pack 03 shensha business logic module."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.constants import (
    SHENSHA_INTERPRETER_ID,
    SHENSHA_INTERPRETER_VERSION,
    SHENSHA_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.models import (
    ShenshaComponentResult,
    ShenshaInterpretationSection,
    ShenshaItemResult,
)

__all__ = [
    "SHENSHA_INTERPRETER_ID",
    "SHENSHA_INTERPRETER_VERSION",
    "SHENSHA_SECTION_TYPE",
    "ShenshaComponentResult",
    "ShenshaFactExtractor",
    "ShenshaFacts",
    "ShenshaInterpretationRuleEngine",
    "ShenshaInterpretationSection",
    "ShenshaInterpreterService",
    "ShenshaItemResult",
    "ShenshaRuleEngineResult",
    "ShenshaRuleLoader",
]


def __getattr__(name: str):
    """Lazy export heavy modules to avoid import cycles."""
    if name in {"ShenshaFactExtractor", "ShenshaFacts"}:
        from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.extractor import (
            ShenshaFactExtractor,
            ShenshaFacts,
        )

        return ShenshaFactExtractor if name == "ShenshaFactExtractor" else ShenshaFacts
    if name in {"ShenshaInterpretationRuleEngine", "ShenshaRuleEngineResult"}:
        from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.rule_engine import (
            ShenshaInterpretationRuleEngine,
            ShenshaRuleEngineResult,
        )

        return (
            ShenshaInterpretationRuleEngine
            if name == "ShenshaInterpretationRuleEngine"
            else ShenshaRuleEngineResult
        )
    if name == "ShenshaRuleLoader":
        from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.rule_loader import (
            ShenshaRuleLoader,
        )

        return ShenshaRuleLoader
    if name == "ShenshaInterpreterService":
        from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.service import (
            ShenshaInterpreterService,
        )

        return ShenshaInterpreterService
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
