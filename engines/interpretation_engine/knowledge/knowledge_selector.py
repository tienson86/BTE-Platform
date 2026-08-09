"""Deterministic released-knowledge selector. No inference."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from engines.interpretation_engine.knowledge.composition_context import (
    COMPOSITION_VERSION,
    CompositionContext,
    resolve_path,
)

STATUS_RELEASED = "released"
STATUS_DRAFT = "draft"


@dataclass(frozen=True, slots=True)
class ReleasedKnowledgeSpec:
    """Selection descriptor for one released knowledge item. Identifiers only."""

    knowledge_id: str
    source: str
    field_path: str
    evidence_id: str
    reasoning_id: str
    reasoning_chain_id: str
    reasoning_graph_id: str
    reasoning_trace_id: str
    template_id: str
    placeholders: tuple[str, ...]
    default_confidence: str
    confidence_path: str | None = None
    module_id: str = "overview"
    status: str = STATUS_RELEASED
    version: str = COMPOSITION_VERSION
    package_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the knowledge spec."""
        return {
            "knowledge_id": self.knowledge_id,
            "source": self.source,
            "field_path": self.field_path,
            "evidence_id": self.evidence_id,
            "reasoning_id": self.reasoning_id,
            "reasoning_chain_id": self.reasoning_chain_id,
            "reasoning_graph_id": self.reasoning_graph_id,
            "reasoning_trace_id": self.reasoning_trace_id,
            "template_id": self.template_id,
            "placeholders": list(self.placeholders),
            "default_confidence": self.default_confidence,
            "confidence_path": self.confidence_path,
            "module_id": self.module_id,
            "status": self.status,
            "version": self.version,
            "package_id": self.package_id,
        }


def default_released_catalog() -> tuple[ReleasedKnowledgeSpec, ...]:
    """Return the frozen IE-2 released selection index. Not package content."""
    return (
        ReleasedKnowledgeSpec(
            knowledge_id="KN-IE2-AN-SEASONAL",
            source="analysis",
            field_path="seasonal.season",
            evidence_id="EV-IE2-AN-SEASONAL",
            reasoning_id="RC-IE2-AN-SEASONAL",
            reasoning_chain_id="RC-IE2-AN-SEASONAL",
            reasoning_graph_id="RG-IE2-AN-SEASONAL",
            reasoning_trace_id="RT-IE2-AN-SEASONAL",
            template_id="TPL-IE2-OVERVIEW-SEASONAL",
            placeholders=("analysis.seasonal.season",),
            default_confidence="high",
            module_id="overview",
        ),
        ReleasedKnowledgeSpec(
            knowledge_id="KN-IE2-AN-USEFUL_GOD",
            source="analysis",
            field_path="useful_god.useful_god",
            evidence_id="EV-IE2-AN-USEFUL_GOD",
            reasoning_id="RC-IE2-AN-USEFUL_GOD",
            reasoning_chain_id="RC-IE2-AN-USEFUL_GOD",
            reasoning_graph_id="RG-IE2-AN-USEFUL_GOD",
            reasoning_trace_id="RT-IE2-AN-USEFUL_GOD",
            template_id="TPL-IE2-OVERVIEW-USEFUL_GOD",
            placeholders=("analysis.useful_god.useful_god",),
            default_confidence="high",
            module_id="overview",
        ),
        ReleasedKnowledgeSpec(
            knowledge_id="KN-IE2-DC-FINAL_UG",
            source="decision",
            field_path="final_useful_god",
            evidence_id="EV-IE2-DC-FINAL_UG",
            reasoning_id="RC-IE2-DC-FINAL_UG",
            reasoning_chain_id="RC-IE2-DC-FINAL_UG",
            reasoning_graph_id="RG-IE2-DC-FINAL_UG",
            reasoning_trace_id="RT-IE2-DC-FINAL_UG",
            template_id="TPL-IE2-SUMMARY-FINAL_UG",
            placeholders=("decision.final_useful_god",),
            default_confidence="high",
            module_id="summary",
        ),
        ReleasedKnowledgeSpec(
            knowledge_id="KN-IE2-LK-PRIORITY",
            source="luck",
            field_path="overall_luck_result.luck_priority.value",
            evidence_id="EV-IE2-LK-PRIORITY",
            reasoning_id="RC-IE2-LK-PRIORITY",
            reasoning_chain_id="RC-IE2-LK-PRIORITY",
            reasoning_graph_id="RG-IE2-LK-PRIORITY",
            reasoning_trace_id="RT-IE2-LK-PRIORITY",
            template_id="TPL-IE2-LUCK-PRIORITY",
            placeholders=("luck.overall_luck_result.luck_priority.value",),
            default_confidence="medium",
            module_id="luck",
        ),
    )


@dataclass(slots=True)
class KnowledgeSelection:
    """Selected released knowledge identity. No generated text."""

    knowledge_id: str
    source: str
    field_path: str
    spec: ReleasedKnowledgeSpec

    def to_dict(self) -> dict[str, Any]:
        """Serialize one knowledge selection."""
        payload = self.spec.to_dict()
        payload["selected"] = True
        return payload


class KnowledgeSelector:
    """Select released knowledge whose published field is present. No inference."""

    def __init__(self, catalog: Sequence[ReleasedKnowledgeSpec] | None = None) -> None:
        """Bind an immutable released catalog."""
        self._catalog = tuple(catalog) if catalog is not None else default_released_catalog()

    @property
    def catalog(self) -> tuple[ReleasedKnowledgeSpec, ...]:
        """Return the bound catalog."""
        return self._catalog

    def select(self, context: CompositionContext) -> tuple[KnowledgeSelection, ...]:
        """Select released items whose contract field resolves to a non-null value."""
        selected: list[KnowledgeSelection] = []
        for spec in sorted(self._catalog, key=lambda item: item.knowledge_id):
            if spec.status != STATUS_RELEASED:
                continue
            snapshot = context.root(spec.source)
            value = resolve_path(snapshot, spec.field_path)
            if value is None:
                continue
            selected.append(
                KnowledgeSelection(
                    knowledge_id=spec.knowledge_id,
                    source=spec.source,
                    field_path=spec.field_path,
                    spec=spec,
                )
            )
        return tuple(selected)
