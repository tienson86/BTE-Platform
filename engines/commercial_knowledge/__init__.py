"""Commercial Knowledge Engine — Wave 1.1 production integration."""

from __future__ import annotations

from .commercial_adapter import CommercialKnowledgeAdapter
from .commercial_bundle import bundle_to_dict
from .models import (
    WAVE_1_1_ALLOW_LIST,
    CommercialKnowledgeBundle,
    NarrativeKnowledgePayload,
    RetrievalRequest,
)
from .narrative_merge import enrich_narrative_inputs
from .retrieval_service import RetrievalService

__all__ = [
    "WAVE_1_1_ALLOW_LIST",
    "CommercialKnowledgeAdapter",
    "CommercialKnowledgeBundle",
    "NarrativeKnowledgePayload",
    "RetrievalRequest",
    "RetrievalService",
    "bundle_to_dict",
    "enrich_narrative_inputs",
]