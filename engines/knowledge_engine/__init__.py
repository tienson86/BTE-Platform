"""Knowledge Engine — classical knowledge through production Knowledge Pipeline.

Milestone 10 integrates Knowledge → Retriever → Reasoning → Evidence →
Prompt → LLM → Validator → Portal without breaking public analyze/UI contracts.
"""

from __future__ import annotations

from engines.knowledge_engine.citation_engine import CitationEngine
from engines.knowledge_engine.citation_models import (
    CLASSICAL_SOURCE_KEYS,
    CLASSICAL_SOURCES,
    Citation,
    CitationPackage,
)
from engines.knowledge_engine.discussion_ai import DiscussionAI
from engines.knowledge_engine.discussion_models import (
    SUPPORTED_QUESTION_TYPES,
    ConversationResult,
    DiscussionAnswer,
)
from engines.knowledge_engine.evidence_builder import EvidenceBuilder
from engines.knowledge_engine.evidence_models import (
    CATEGORY_LABELS,
    EVIDENCE_CATEGORIES,
    EvidenceItem,
    EvidencePackage,
)
from engines.knowledge_engine.exceptions import (
    KnowledgeEngineError,
    KnowledgeLoadError,
    KnowledgeSchemaError,
)
from engines.knowledge_engine.llm import DeterministicKnowledgeLLM
from engines.knowledge_engine.loader import KnowledgeLoader
from engines.knowledge_engine.models import (
    KNOWLEDGE_FILES,
    REQUIRED_COLUMNS,
    KnowledgeHit,
    KnowledgeRecord,
    KnowledgeResult,
    RetrievalTraceEntry,
)
from engines.knowledge_engine.pipeline import (
    PIPELINE_STAGES,
    PIPELINE_VERSION,
    KnowledgePipeline,
    KnowledgePipelineResult,
)
from engines.knowledge_engine.prompt_builder import PromptBuilder
from engines.knowledge_engine.prompt_models import (
    PROMPT_SECTION_KEYS,
    PROMPT_SECTION_TITLES,
    PromptSection,
    StructuredPrompt,
)
from engines.knowledge_engine.reasoning_graph import ReasoningGraphEngine
from engines.knowledge_engine.reasoning_models import (
    ReasoningEdge,
    ReasoningGraph,
    ReasoningNode,
)
from engines.knowledge_engine.repository import KnowledgeRepository
from engines.knowledge_engine.response_validator import AIResponseValidator
from engines.knowledge_engine.retriever import KnowledgeRetriever
from engines.knowledge_engine.validation_models import (
    VALIDATION_CHECKS,
    ParagraphValidation,
    ValidationReport,
    ValidationWarning,
)

__all__ = [
    "AIResponseValidator",
    "CATEGORY_LABELS",
    "CLASSICAL_SOURCE_KEYS",
    "CLASSICAL_SOURCES",
    "Citation",
    "CitationEngine",
    "CitationPackage",
    "ConversationResult",
    "DeterministicKnowledgeLLM",
    "DiscussionAI",
    "DiscussionAnswer",
    "EVIDENCE_CATEGORIES",
    "EvidenceBuilder",
    "EvidenceItem",
    "EvidencePackage",
    "KNOWLEDGE_FILES",
    "KnowledgePipeline",
    "KnowledgePipelineResult",
    "PIPELINE_STAGES",
    "PIPELINE_VERSION",
    "PROMPT_SECTION_KEYS",
    "PROMPT_SECTION_TITLES",
    "PromptBuilder",
    "PromptSection",
    "ParagraphValidation",
    "REQUIRED_COLUMNS",
    "SUPPORTED_QUESTION_TYPES",
    "StructuredPrompt",
    "VALIDATION_CHECKS",
    "ValidationReport",
    "ValidationWarning",
    "KnowledgeEngineError",
    "KnowledgeHit",
    "KnowledgeLoadError",
    "KnowledgeLoader",
    "KnowledgeRecord",
    "KnowledgeRepository",
    "KnowledgeResult",
    "KnowledgeRetriever",
    "KnowledgeSchemaError",
    "ReasoningEdge",
    "ReasoningGraph",
    "ReasoningGraphEngine",
    "ReasoningNode",
    "RetrievalTraceEntry",
]
