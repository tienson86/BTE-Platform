"""Deterministic template identifier selection. No rendering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from engines.interpretation_engine.knowledge.knowledge_selector import KnowledgeSelection


@dataclass(slots=True)
class TemplateSelection:
    """Selected template identifier. Body is never loaded."""

    template_id: str
    knowledge_id: str
    module_id: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one template selection."""
        return {
            "template_id": self.template_id,
            "knowledge_id": self.knowledge_id,
            "module_id": self.module_id,
        }


class TemplateSelector:
    """Select template identifiers only. No formatting or prose."""

    def select(self, knowledge: Sequence[KnowledgeSelection]) -> tuple[TemplateSelection, ...]:
        """Emit template ids for selected knowledge, sorted by template_id."""
        selected = [
            TemplateSelection(
                template_id=item.spec.template_id,
                knowledge_id=item.knowledge_id,
                module_id=item.spec.module_id,
            )
            for item in knowledge
        ]
        return tuple(sorted(selected, key=lambda item: (item.template_id, item.knowledge_id)))
