"""Knowledge Engine — classical knowledge, retrieval, reasoning, evidence, prompts.

Milestone 06 adds Prompt Builder for structured AI prompts.
"""

from __future__ import annotations

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
from engines.knowledge_engine.loader import KnowledgeLoader
from engines.knowledge_engine.models import (
    KNOWLEDGE_FILES,
    REQUIRED_COLUMNS,
    KnowledgeHit,
    KnowledgeRecord,
    KnowledgeResult,
    RetrievalTraceEntry,
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
from engines.knowledge_engine.retriever import KnowledgeRetriever

__all__ = [
    "CATEGORY_LABELS",
    "EVIDENCE_CATEGORIES",
    "EvidenceBuilder",
    "EvidenceItem",
    "EvidencePackage",
    "KNOWLEDGE_FILES",
    "PROMPT_SECTION_KEYS",
    "PROMPT_SECTION_TITLES",
    "PromptBuilder",
    "PromptSection",
    "REQUIRED_COLUMNS",
    "StructuredPrompt",
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
