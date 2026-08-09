"""IE-2 Knowledge Selection & Sentence Composition Engine."""

from engines.interpretation_engine.knowledge.composition_context import (
    COMPOSITION_VERSION,
    CompositionContext,
    build_composition_context,
)
from engines.interpretation_engine.knowledge.composition_result import (
    CompositionResult,
    SentenceCandidate,
)
from engines.interpretation_engine.knowledge.evidence_selector import EvidenceSelector
from engines.interpretation_engine.knowledge.knowledge_selector import KnowledgeSelector
from engines.interpretation_engine.knowledge.placeholder_binder import PlaceholderBinder
from engines.interpretation_engine.knowledge.reasoning_selector import ReasoningSelector
from engines.interpretation_engine.knowledge.selector_registry import SelectorRegistry
from engines.interpretation_engine.knowledge.sentence_candidate_builder import (
    SentenceCandidateBuilder,
)
from engines.interpretation_engine.knowledge.template_selector import TemplateSelector

__all__ = [
    "COMPOSITION_VERSION",
    "CompositionContext",
    "CompositionResult",
    "EvidenceSelector",
    "KnowledgeSelector",
    "PlaceholderBinder",
    "ReasoningSelector",
    "SelectorRegistry",
    "SentenceCandidate",
    "SentenceCandidateBuilder",
    "TemplateSelector",
    "build_composition_context",
]
