"""Ten Gods Interpreter package — Pack 03 ten-gods business logic module."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.constants import (
    TEN_GODS_INTERPRETER_ID,
    TEN_GODS_INTERPRETER_VERSION,
    TEN_GODS_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.models import (
    TenGodsComponentResult,
    TenGodsInterpretationSection,
    TenGodsItemResult,
)

__all__ = [
    "TEN_GODS_INTERPRETER_ID",
    "TEN_GODS_INTERPRETER_VERSION",
    "TEN_GODS_SECTION_TYPE",
    "TenGodsComponentResult",
    "TenGodsFactExtractor",
    "TenGodsFacts",
    "TenGodsInterpretationRuleEngine",
    "TenGodsInterpretationSection",
    "TenGodsInterpreterService",
    "TenGodsItemResult",
    "TenGodsRuleEngineResult",
    "TenGodsRuleLoader",
]


def __getattr__(name: str):
    """Lazy export heavy modules to avoid import cycles."""
    if name in {"TenGodsFactExtractor", "TenGodsFacts"}:
        from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.extractor import (
            TenGodsFactExtractor,
            TenGodsFacts,
        )

        return TenGodsFactExtractor if name == "TenGodsFactExtractor" else TenGodsFacts
    if name in {"TenGodsInterpretationRuleEngine", "TenGodsRuleEngineResult"}:
        from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.rule_engine import (
            TenGodsInterpretationRuleEngine,
            TenGodsRuleEngineResult,
        )

        return (
            TenGodsInterpretationRuleEngine
            if name == "TenGodsInterpretationRuleEngine"
            else TenGodsRuleEngineResult
        )
    if name == "TenGodsRuleLoader":
        from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.rule_loader import (
            TenGodsRuleLoader,
        )

        return TenGodsRuleLoader
    if name == "TenGodsInterpreterService":
        from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.service import (
            TenGodsInterpreterService,
        )

        return TenGodsInterpreterService
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
