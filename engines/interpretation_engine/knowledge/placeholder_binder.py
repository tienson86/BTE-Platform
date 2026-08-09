"""Bind placeholders to published Canonical Result fields only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from engines.interpretation_engine.knowledge.composition_context import (
    CompositionContext,
    PlaceholderIntegrityError,
)
from engines.interpretation_engine.knowledge.knowledge_selector import KnowledgeSelection
from engines.interpretation_engine.knowledge.template_selector import TemplateSelection

STATUS_BOUND = "bound"
STATUS_UNBOUND = "unbound"


@dataclass(slots=True)
class PlaceholderBinding:
    """Resolved placeholder value copied from a published contract field."""

    placeholder_id: str
    binding_path: str
    value: Any
    source: str
    status: str
    knowledge_id: str
    template_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize one placeholder binding."""
        return {
            "placeholder_id": self.placeholder_id,
            "binding_path": self.binding_path,
            "value": self.value,
            "source": self.source,
            "status": self.status,
            "knowledge_id": self.knowledge_id,
            "template_id": self.template_id,
        }


class PlaceholderBinder:
    """Resolve placeholders using Canonical Results. No computed fields."""

    def bind(
        self,
        context: CompositionContext,
        knowledge: Sequence[KnowledgeSelection],
        templates: Sequence[TemplateSelection] | None = None,
    ) -> tuple[PlaceholderBinding, ...]:
        """Bind declared placeholder paths. Unpublished paths fail closed."""
        template_by_knowledge = {
            item.knowledge_id: item.template_id for item in (templates or ())
        }
        bindings: list[PlaceholderBinding] = []
        seen: set[tuple[str, str]] = set()
        for item in knowledge:
            for path in item.spec.placeholders:
                key = (item.knowledge_id, path)
                if key in seen:
                    continue
                seen.add(key)
                source = path.split(".", 1)[0]
                try:
                    value = context.resolve_published(path)
                    status = STATUS_BOUND if value is not None else STATUS_UNBOUND
                except PlaceholderIntegrityError:
                    raise
                bindings.append(
                    PlaceholderBinding(
                        placeholder_id=f"PH-{item.knowledge_id}-{path}",
                        binding_path=path,
                        value=value,
                        source=source,
                        status=status,
                        knowledge_id=item.knowledge_id,
                        template_id=template_by_knowledge.get(item.knowledge_id),
                    )
                )
        return tuple(sorted(bindings, key=lambda item: item.placeholder_id))
