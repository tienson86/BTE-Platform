"""IE-2 composition result. Structured candidates only. No paragraphs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from engines.interpretation_engine.knowledge.composition_context import (
    AI_REWRITE_ENABLED,
    COMPOSITION_ENGINE_ID,
    COMPOSITION_VERSION,
)
from engines.interpretation_engine.knowledge.evidence_selector import EvidenceBundle
from engines.interpretation_engine.knowledge.knowledge_selector import KnowledgeSelection
from engines.interpretation_engine.knowledge.placeholder_binder import PlaceholderBinding
from engines.interpretation_engine.knowledge.reasoning_selector import ReasoningSelection
from engines.interpretation_engine.knowledge.template_selector import TemplateSelection


@dataclass(slots=True)
class SentenceCandidate:
    """Structured sentence candidate. Not a human-readable paragraph."""

    sentence_id: str
    template_id: str
    placeholder_values: dict[str, Any]
    evidence_ids: tuple[str, ...]
    reasoning_ids: tuple[str, ...]
    confidence: str
    references: tuple[str, ...]
    knowledge_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize one sentence candidate."""
        return {
            "sentence_id": self.sentence_id,
            "template_id": self.template_id,
            "placeholder_values": dict(self.placeholder_values),
            "evidence_ids": list(self.evidence_ids),
            "reasoning_ids": list(self.reasoning_ids),
            "confidence": self.confidence,
            "references": list(self.references),
            "knowledge_id": self.knowledge_id,
        }


@dataclass(slots=True)
class CompositionResult:
    """Official IE-2 selection output consumed by IE-3."""

    composition_version: str = COMPOSITION_VERSION
    engine_id: str = COMPOSITION_ENGINE_ID
    success: bool = True
    knowledge: tuple[KnowledgeSelection, ...] = ()
    evidence: tuple[EvidenceBundle, ...] = ()
    reasoning: tuple[ReasoningSelection, ...] = ()
    templates: tuple[TemplateSelection, ...] = ()
    placeholders: tuple[PlaceholderBinding, ...] = ()
    candidates: tuple[SentenceCandidate, ...] = ()
    diagnostics: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()
    ai_rewrite: Mapping[str, Any] = field(
        default_factory=lambda: {
            "enabled": AI_REWRITE_ENABLED,
            "status": "disabled",
            "hook": "future_ie3_ai_rewrite",
        }
    )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the composition result."""
        return {
            "composition_version": self.composition_version,
            "engine_id": self.engine_id,
            "success": self.success,
            "knowledge": [item.to_dict() for item in self.knowledge],
            "evidence": [item.to_dict() for item in self.evidence],
            "reasoning": [item.to_dict() for item in self.reasoning],
            "templates": [item.to_dict() for item in self.templates],
            "placeholders": [item.to_dict() for item in self.placeholders],
            "candidates": [item.to_dict() for item in self.candidates],
            "diagnostics": list(self.diagnostics),
            "errors": list(self.errors),
            "ai_rewrite": dict(self.ai_rewrite),
        }


def build_composition_result(
    *,
    knowledge: Sequence[KnowledgeSelection],
    evidence: Sequence[EvidenceBundle],
    reasoning: Sequence[ReasoningSelection],
    templates: Sequence[TemplateSelection],
    placeholders: Sequence[PlaceholderBinding],
    candidates: Sequence[SentenceCandidate],
    success: bool,
    diagnostics: Sequence[str],
    errors: Sequence[str] = (),
) -> CompositionResult:
    """Assemble the IE-2 composition result."""
    return CompositionResult(
        success=success,
        knowledge=tuple(knowledge),
        evidence=tuple(evidence),
        reasoning=tuple(reasoning),
        templates=tuple(templates),
        placeholders=tuple(placeholders),
        candidates=tuple(candidates),
        diagnostics=tuple(diagnostics),
        errors=tuple(errors),
    )
