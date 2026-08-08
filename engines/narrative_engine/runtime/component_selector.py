"""Component selection for Narrative Runtime (Sprint D1)."""

from __future__ import annotations

import logging

from .models import (
    COMPONENT_EVIDENCE_KINDS,
    OFFICIAL_COMPONENT_ORDER,
    ComponentType,
    RuntimeEvidenceUnit,
    RuntimeInput,
    RuntimeInterpretationRef,
)

logger = logging.getLogger(__name__)


class ComponentSelector:
    """
    Select evidence and interpretation refs for each component type.

    Structural binding only — no wording.
    """

    def select(
        self,
        evidence: tuple[RuntimeEvidenceUnit, ...],
        runtime_input: RuntimeInput,
    ) -> dict[ComponentType, tuple[tuple[str, ...], tuple[str, ...]]]:
        """
        Return mapping component → (evidence_ids, interpretation_ids).

        Every official component appears in the mapping.
        """
        interp_refs = tuple(
            ref
            for ref in runtime_input.interpretation_refs
            if (ref.id or "").strip() and ref.commercial_ok
        )
        selected: dict[ComponentType, tuple[tuple[str, ...], tuple[str, ...]]] = {}
        for component in OFFICIAL_COMPONENT_ORDER:
            evidence_ids = _select_evidence_ids(component, evidence)
            interpretation_ids = _select_interpretation_ids(component, interp_refs)
            selected[component] = (evidence_ids, interpretation_ids)
            logger.debug(
                "component_selector.%s evidence=%s interp=%s",
                component.value,
                len(evidence_ids),
                len(interpretation_ids),
            )
        return selected


def _select_evidence_ids(
    component: ComponentType,
    evidence: tuple[RuntimeEvidenceUnit, ...],
) -> tuple[str, ...]:
    """Pick evidence ids whose kind is allowed for the component."""
    allowed = COMPONENT_EVIDENCE_KINDS[component]
    ids: list[str] = []
    for unit in evidence:
        if not unit.commercial_ok:
            continue
        if unit.kind in allowed:
            ids.append(unit.id)
    return tuple(ids)


def _select_interpretation_ids(
    component: ComponentType,
    refs: tuple[RuntimeInterpretationRef, ...],
) -> tuple[str, ...]:
    """Pick interpretation refs using intent hints / title heuristics (ids only)."""
    if not refs:
        return ()
    needle_map: dict[ComponentType, tuple[str, ...]] = {
        ComponentType.EXECUTIVE_SUMMARY: ("tổng quan", "kết luận", "summary", "executive"),
        ComponentType.OBSERVATION: ("tính cách", "tổng quan", "overview", "observation"),
        ComponentType.REASONING: ("lý giải", "reasoning", "giải thích", "explanation"),
        ComponentType.IMPACT: ("ảnh hưởng", "impact", "ý nghĩa"),
        ComponentType.RECOMMENDATION: ("dụng thần", "khuyến", "hành động", "recommend"),
        ComponentType.WARNING: ("lưu ý", "warning", "nhược", "rủi ro"),
        ComponentType.CONCLUSION: ("kết luận", "conclusion", "tóm"),
    }
    needles = needle_map[component]
    matched: list[str] = []
    for ref in refs:
        blob = " ".join(
            (
                ref.section_id,
                ref.title,
                " ".join(ref.intent_hints),
            )
        ).lower()
        if any(token in blob for token in needles):
            matched.append(ref.id)
    # Executive / Conclusion may fall back to all commercial refs for structure only.
    if not matched and component in {
        ComponentType.EXECUTIVE_SUMMARY,
        ComponentType.CONCLUSION,
    }:
        return tuple(ref.id for ref in refs[:3])
    return tuple(matched)
