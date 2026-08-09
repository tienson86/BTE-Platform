"""Deterministic evidence selection. No synthesis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from engines.interpretation_engine.knowledge.composition_context import (
    CompositionContext,
    resolve_path,
)
from engines.interpretation_engine.knowledge.knowledge_selector import KnowledgeSelection

CONFIDENCE_NONE = "none"


@dataclass(slots=True)
class EvidenceBundle:
    """Resolved evidence identity, confidence, references, and boundary flag."""

    evidence_id: str
    knowledge_id: str
    confidence: str
    references: tuple[str, ...]
    boundary: bool
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one evidence bundle."""
        return {
            "evidence_id": self.evidence_id,
            "knowledge_id": self.knowledge_id,
            "confidence": self.confidence,
            "references": list(self.references),
            "boundary": self.boundary,
            "status": self.status,
        }


def _declared_confidence(value: Any, default_confidence: str) -> str:
    """Copy a published confidence token. Do not compute a new score."""
    if value is None:
        return CONFIDENCE_NONE
    if isinstance(value, str) and value:
        return value
    if isinstance(value, dict) and value.get("value"):
        return str(value["value"])
    return default_confidence


class EvidenceSelector:
    """Resolve evidence bundles from selected released knowledge only."""

    def select(
        self,
        context: CompositionContext,
        knowledge: Sequence[KnowledgeSelection],
    ) -> tuple[EvidenceBundle, ...]:
        """Emit one evidence bundle per selected knowledge item."""
        bundles: list[EvidenceBundle] = []
        for item in knowledge:
            spec = item.spec
            references = (f"{spec.source}.{spec.field_path}",)
            boundary = False
            if spec.confidence_path:
                confidence_value = resolve_path(context.root(spec.source), spec.confidence_path)
                if confidence_value is None:
                    boundary = True
                    confidence = CONFIDENCE_NONE
                else:
                    confidence = _declared_confidence(
                        confidence_value,
                        spec.default_confidence,
                    )
            else:
                confidence = spec.default_confidence
            bundles.append(
                EvidenceBundle(
                    evidence_id=spec.evidence_id,
                    knowledge_id=spec.knowledge_id,
                    confidence=confidence,
                    references=references,
                    boundary=boundary,
                    status="boundary" if boundary else "resolved",
                )
            )
        return tuple(sorted(bundles, key=lambda item: item.evidence_id))
