"""PACK_05 Narrative Composer — Sprint D2 (NarrativeTree → NarrativeResult)."""

from __future__ import annotations

from .composer import NarrativeResultComposer
from .models import (
    NarrativeParagraph,
    NarrativeRecommendation,
    NarrativeResult,
    NarrativeSection,
    NarrativeSummary,
    ParagraphRole,
    RecommendationPriority,
    ResultStatus,
)
from .constants import INSUFFICIENT_EVIDENCE_NARRATIVE

__all__ = [
    "INSUFFICIENT_EVIDENCE_NARRATIVE",
    "NarrativeParagraph",
    "NarrativeRecommendation",
    "NarrativeResult",
    "NarrativeResultComposer",
    "NarrativeSection",
    "NarrativeSummary",
    "ParagraphRole",
    "RecommendationPriority",
    "ResultStatus",
]
