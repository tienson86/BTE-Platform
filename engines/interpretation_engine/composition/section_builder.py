"""Deterministic section builder. Structure only. No rendering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from engines.interpretation_engine.composition.composition_context import (
    InterpretationAssemblyContext,
)
from engines.interpretation_engine.foundation_constants import CANONICAL_MODULE_ORDER


@dataclass(slots=True)
class AssembledSection:
    """Structural section assembled from sentence candidates."""

    section_id: str
    module_id: str
    candidate_ids: tuple[str, ...]
    knowledge_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    reasoning_ids: tuple[str, ...]
    template_ids: tuple[str, ...]
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one assembled section."""
        return {
            "section_id": self.section_id,
            "module_id": self.module_id,
            "candidate_ids": list(self.candidate_ids),
            "knowledge_ids": list(self.knowledge_ids),
            "evidence_ids": list(self.evidence_ids),
            "reasoning_ids": list(self.reasoning_ids),
            "template_ids": list(self.template_ids),
            "status": self.status,
        }


def _module_index() -> dict[str, int]:
    return {module_id: index for index, module_id in enumerate(CANONICAL_MODULE_ORDER)}


def _template_module_map(selection: Mapping[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for item in selection.get("templates") or ():
        if isinstance(item, Mapping) and item.get("knowledge_id") and item.get("module_id"):
            mapping[str(item["knowledge_id"])] = str(item["module_id"])
    for item in selection.get("knowledge") or ():
        if not isinstance(item, Mapping):
            continue
        knowledge_id = str(item.get("knowledge_id") or "")
        module_id = str(item.get("module_id") or "")
        if knowledge_id and module_id:
            mapping.setdefault(knowledge_id, module_id)
    return mapping


class SectionBuilder:
    """Group sentence candidates into sections. No styling or formatting."""

    def build(self, context: InterpretationAssemblyContext) -> tuple[AssembledSection, ...]:
        """Build one section per module that has at least one candidate."""
        module_of = _template_module_map(context.selection_snapshot())
        grouped: dict[str, list[dict[str, Any]]] = {}
        for candidate in context.candidates():
            knowledge_id = str(candidate.get("knowledge_id") or "")
            module_id = module_of.get(knowledge_id)
            if module_id not in _module_index():
                continue
            grouped.setdefault(module_id, []).append(candidate)
        sections: list[AssembledSection] = []
        for module_id, _index in sorted(_module_index().items(), key=lambda item: item[1]):
            rows = grouped.get(module_id) or []
            if not rows:
                continue
            evidence_ids: list[str] = []
            reasoning_ids: list[str] = []
            template_ids: list[str] = []
            knowledge_ids: list[str] = []
            candidate_ids: list[str] = []
            for row in rows:
                candidate_id = str(row.get("sentence_id") or "")
                if candidate_id:
                    candidate_ids.append(candidate_id)
                knowledge_id = str(row.get("knowledge_id") or "")
                if knowledge_id:
                    knowledge_ids.append(knowledge_id)
                template_id = str(row.get("template_id") or "")
                if template_id:
                    template_ids.append(template_id)
                evidence_ids.extend(str(item) for item in row.get("evidence_ids") or ())
                reasoning_ids.extend(str(item) for item in row.get("reasoning_ids") or ())
            sections.append(
                AssembledSection(
                    section_id=f"SEC-{module_id}",
                    module_id=module_id,
                    candidate_ids=tuple(candidate_ids),
                    knowledge_ids=tuple(dict.fromkeys(knowledge_ids)),
                    evidence_ids=tuple(dict.fromkeys(evidence_ids)),
                    reasoning_ids=tuple(dict.fromkeys(reasoning_ids)),
                    template_ids=tuple(dict.fromkeys(template_ids)),
                    status="assembled",
                )
            )
        return tuple(sections)
