"""Logical flow optimizer. Ordering and grouping only. No rewriting."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from engines.interpretation_engine.composition.chapter_builder import AssembledChapter
from engines.interpretation_engine.composition.section_builder import AssembledSection
from engines.interpretation_engine.foundation_constants import (
    CANONICAL_MODULE_ORDER,
    MODULE_OVERVIEW,
    MODULE_SUMMARY,
)


@dataclass(slots=True)
class FlowPlan:
    """Machine-readable flow plan after ordering and grouping."""

    section_order: tuple[str, ...]
    chapter_order: tuple[str, ...]
    groups: tuple[tuple[str, ...], ...]
    dependencies: tuple[tuple[str, str], ...]
    operations: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the flow plan."""
        return {
            "section_order": list(self.section_order),
            "chapter_order": list(self.chapter_order),
            "groups": [list(group) for group in self.groups],
            "dependencies": [list(item) for item in self.dependencies],
            "operations": list(self.operations),
        }


def _module_rank() -> dict[str, int]:
    return {module_id: index for index, module_id in enumerate(CANONICAL_MODULE_ORDER)}


class FlowOptimizer:
    """Restore canonical section/chapter order. No paraphrase or summary."""

    def optimize(
        self,
        sections: Sequence[AssembledSection],
        chapters: Sequence[AssembledChapter],
    ) -> tuple[tuple[AssembledSection, ...], tuple[AssembledChapter, ...], FlowPlan]:
        """Order and group by registered module dependencies."""
        rank = _module_rank()
        sorted_sections = tuple(sorted(sections, key=lambda item: rank.get(item.module_id, 99)))
        sorted_chapters = tuple(
            AssembledChapter(
                chapter_id=chapter.chapter_id,
                module_id=chapter.module_id,
                section_ids=tuple(
                    section.section_id
                    for section in sorted_sections
                    if section.module_id == chapter.module_id
                ),
                sequence=rank.get(chapter.module_id, chapter.sequence),
                status=chapter.status if any(
                    section.module_id == chapter.module_id for section in sorted_sections
                ) else "empty",
            )
            for chapter in sorted(chapters, key=lambda item: rank.get(item.module_id, 99))
        )
        overview = tuple(
            item.section_id for item in sorted_sections if item.module_id == MODULE_OVERVIEW
        )
        middle = tuple(
            item.section_id
            for item in sorted_sections
            if item.module_id not in {MODULE_OVERVIEW, MODULE_SUMMARY}
        )
        summary = tuple(
            item.section_id for item in sorted_sections if item.module_id == MODULE_SUMMARY
        )
        groups = tuple(group for group in (overview, middle, summary) if group)
        dependencies = tuple(
            (MODULE_OVERVIEW, module_id)
            for module_id in CANONICAL_MODULE_ORDER
            if module_id != MODULE_OVERVIEW
        ) + tuple(
            (module_id, MODULE_SUMMARY)
            for module_id in CANONICAL_MODULE_ORDER
            if module_id != MODULE_SUMMARY
        )
        plan = FlowPlan(
            section_order=tuple(item.section_id for item in sorted_sections),
            chapter_order=tuple(item.chapter_id for item in sorted_chapters),
            groups=groups,
            dependencies=dependencies,
            operations=("order_by_module", "group_overview_body_summary"),
        )
        return sorted_sections, sorted_chapters, plan
