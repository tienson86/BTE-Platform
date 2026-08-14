"""Interpretation Foundation (Sprint A) — canonical contracts over engine truth."""

from engines.interpretation_engine.foundation.service import (
    InterpretationFoundationBundle,
    build_interpretation_foundation,
)
from engines.interpretation_engine.foundation.canonical_context import (
    CanonicalAnalysisContext,
)
from engines.interpretation_engine.foundation.builders.engine_sources import EngineSources

__all__ = [
    "CanonicalAnalysisContext",
    "EngineSources",
    "InterpretationFoundationBundle",
    "build_interpretation_foundation",
]
