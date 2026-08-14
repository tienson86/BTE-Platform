"""Interpretation Foundation (Sprint A) — canonical contracts over engine truth."""

from engines.interpretation_engine.foundation.service import (
    InterpretationFoundationBundle,
    build_interpretation_foundation,
)
from engines.interpretation_engine.foundation.canonical_context import (
    CanonicalAnalysisContext,
)
from engines.interpretation_engine.foundation.builders.engine_sources import EngineSources
from engines.interpretation_engine.foundation.explanation.models import (
    DecisionExplanationResult,
)
from engines.interpretation_engine.foundation.explanation import (
    DecisionExplainer,
    validate_decision_explanation,
)
from engines.interpretation_engine.foundation.interpreters.useful_god import (
    UsefulGodInterpreter,
    UsefulGodInterpretationResult,
)

__all__ = [
    "CanonicalAnalysisContext",
    "DecisionExplanationResult",
    "DecisionExplainer",
    "EngineSources",
    "InterpretationFoundationBundle",
    "UsefulGodInterpreter",
    "UsefulGodInterpretationResult",
    "build_interpretation_foundation",
    "validate_decision_explanation",
]
