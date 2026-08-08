"""Composition source bundle — factual payloads for D2 (no invention)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engines.narrative_engine.runtime.models import EvidenceKind, NarrativeTree


@dataclass(slots=True)
class SourceFact:
    """
    One traceable fact available to the composer.

    Text must come from Interpretation / Evidence / Rule / Knowledge sources.
    """

    id: str
    kind: str
    label: str = ""
    value: str = ""
    raw_text: str = ""
    source_path: str = ""
    rule_refs: tuple[str, ...] = ()
    knowledge_refs: tuple[str, ...] = ()
    confidence: float = 0.0
    commercial_ok: bool = True

    def display_value(self) -> str:
        """Return the best non-invented display string for this fact."""
        text = (self.raw_text or "").strip()
        if text:
            return text
        value = (self.value or "").strip()
        label = (self.label or "").strip()
        if label and value:
            return f"{label}: {value}"
        return value or label


@dataclass(slots=True)
class CompositionSource:
    """All factual sources needed to render NarrativeTree → NarrativeResult."""

    tree: NarrativeTree
    facts: dict[str, SourceFact] = field(default_factory=dict)
    interpretation_facts: dict[str, SourceFact] = field(default_factory=dict)
    analysis: Any = None
    interpretation: Any = None

    def fact(self, fact_id: str) -> SourceFact | None:
        """Lookup evidence or interpretation fact by id."""
        if fact_id in self.facts:
            return self.facts[fact_id]
        return self.interpretation_facts.get(fact_id)

    def commercial_facts(self, ids: tuple[str, ...]) -> tuple[SourceFact, ...]:
        """Return commercial-ok facts for the given ids (order preserved)."""
        selected: list[SourceFact] = []
        for fact_id in ids:
            item = self.fact(fact_id)
            if item is None:
                continue
            if not item.commercial_ok:
                continue
            if not item.display_value().strip():
                continue
            selected.append(item)
        return tuple(selected)
