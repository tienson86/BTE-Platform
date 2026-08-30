"""Narrative V2 Knowledge Resolver public surface."""

from __future__ import annotations

from engines.narrative_v2.knowledge.knowledge_context import (
    KnowledgeContractGap,
    KnowledgeMatch,
    KnowledgeUnresolved,
    NarrativeKnowledgeContext,
)
from engines.narrative_v2.knowledge.knowledge_errors import (
    KnowledgeError,
    KnowledgeValidationError,
)
from engines.narrative_v2.knowledge.knowledge_index import IndexedKnowledge, KnowledgeIndex
from engines.narrative_v2.knowledge.knowledge_item import KnowledgeItem
from engines.narrative_v2.knowledge.knowledge_loader import KnowledgeLoader
from engines.narrative_v2.knowledge.knowledge_reference import KnowledgeReference
from engines.narrative_v2.knowledge.knowledge_registry import KnowledgeRegistry
from engines.narrative_v2.knowledge.knowledge_resolver import KnowledgeResolver
from engines.narrative_v2.knowledge.knowledge_status import (
    ALLOWED_KNOWLEDGE_TYPES,
    ELIGIBLE_SOURCE_STATUSES,
    RESOLVER_VERSION,
)
from engines.narrative_v2.knowledge.knowledge_validator import (
    KnowledgeValidationOutcome,
    KnowledgeValidator,
)

__all__ = [
    "ALLOWED_KNOWLEDGE_TYPES",
    "ELIGIBLE_SOURCE_STATUSES",
    "RESOLVER_VERSION",
    "IndexedKnowledge",
    "KnowledgeContractGap",
    "KnowledgeError",
    "KnowledgeIndex",
    "KnowledgeItem",
    "KnowledgeLoader",
    "KnowledgeMatch",
    "KnowledgeReference",
    "KnowledgeRegistry",
    "KnowledgeResolver",
    "KnowledgeUnresolved",
    "KnowledgeValidationError",
    "KnowledgeValidationOutcome",
    "KnowledgeValidator",
    "NarrativeKnowledgeContext",
]
