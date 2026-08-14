"""Retrieve interpretation knowledge for decision explainers."""

from __future__ import annotations

from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.knowledge.registry import KnowledgeRegistry

_default_registry: KnowledgeRegistry | None = None


def get_knowledge_registry() -> KnowledgeRegistry:
    """Return shared default knowledge registry."""
    global _default_registry
    if _default_registry is None:
        _default_registry = KnowledgeRegistry.default()
    return _default_registry


def retrieve_knowledge(domain: str, key: str) -> KnowledgeEntity | None:
    """Lookup expert knowledge by domain and key."""
    return get_knowledge_registry().get(domain, key)
