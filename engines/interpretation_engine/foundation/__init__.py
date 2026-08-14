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
from engines.interpretation_engine.foundation.concepts import (
    ConceptEntity,
    ConceptRegistry,
    retrieve_concept,
    retrieve_concepts_for_knowledge,
)
from engines.interpretation_engine.foundation.knowledge import (
    KnowledgeEntity,
    KnowledgeRegistry,
    retrieve_knowledge,
)
from engines.interpretation_engine.foundation.interpreters.useful_god import (
    UsefulGodInterpreter,
    UsefulGodInterpretationResult,
)

__all__ = [
    "CanonicalAnalysisContext",
    "ConceptEntity",
    "ConceptRegistry",
    "DecisionExplanationResult",
    "DecisionExplainer",
    "EngineSources",
    "InterpretationFoundationBundle",
    "KnowledgeEntity",
    "KnowledgeRegistry",
    "UsefulGodInterpreter",
    "UsefulGodInterpretationResult",
    "build_interpretation_foundation",
    "retrieve_concept",
    "retrieve_concepts_for_knowledge",
    "retrieve_knowledge",
    "validate_decision_explanation",
]
