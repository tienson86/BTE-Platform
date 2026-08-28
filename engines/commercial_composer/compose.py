"""Compose CommercialNarrativeUnit by applying frozen INT-03B editorial rules."""

from __future__ import annotations

from typing import Any

from engines.commercial_composer.contracts import COMMERCIAL_SECTIONS
from engines.commercial_composer.editor import (
    clean_lines,
    dedupe_lines,
    first_cleaned,
    merge_recommendations,
    select_executive,
)
from engines.commercial_composer.mapping import (
    as_record,
    iter_integrated_lines,
    lines_for_section,
    to_sentences,
)
from engines.commercial_composer.models import (
    CommercialNarrativeBlock,
    CommercialNarrativeUnit,
    empty_commercial_block,
)
from engines.commercial_composer.rules import CUSTOMER_SECTION_ORDER


def compose_commercial_narrative(integrated: Any = None) -> CommercialNarrativeUnit:
    """Edit Integrated Narrative into Commercial Narrative. Does not author facts."""
    payload = as_record(integrated)
    blocks = {
        "executive_summary": _block("executive_summary", _executive_lines(payload)),
        "overall_reading": empty_commercial_block("overall_reading"),
        "current_situation": _section("current_situation", payload, dedupe=True),
        "strengths": _section("strengths", payload, dedupe=True),
        "risks": _section("risks", payload, dedupe=True),
        "key_recommendation": _block(
            "key_recommendation",
            merge_recommendations(lines_for_section(payload, "key_recommendation")),
        ),
        "conclusion": _block("conclusion", _conclusion_lines(payload)),
    }
    refs = tuple(
        path
        for slot in COMMERCIAL_SECTIONS
        for sentence in blocks[slot].sentences
        for path in sentence.source_paths
    )
    return CommercialNarrativeUnit(
        executive_summary=blocks["executive_summary"],
        overall_reading=blocks["overall_reading"],
        current_situation=blocks["current_situation"],
        strengths=blocks["strengths"],
        risks=blocks["risks"],
        key_recommendation=blocks["key_recommendation"],
        conclusion=blocks["conclusion"],
        status=_status(blocks),
        evidence_refs=refs,
    )


def _executive_lines(payload: dict[str, Any]) -> tuple:
    """C-001: select from published findings, not concatenated topic summaries."""
    candidates = iter_integrated_lines(payload, "executive_summary") + iter_integrated_lines(
        payload,
        "observation",
    )
    return select_executive(candidates)


def _conclusion_lines(payload: dict[str, Any]) -> tuple:
    """Restate first cleaned summary sentence plus strongest published recommendation."""
    summary = first_cleaned(iter_integrated_lines(payload, "summary"))
    recommendation = merge_recommendations(iter_integrated_lines(payload, "recommendation"))[:1]
    return dedupe_lines(summary + recommendation)


def _section(slot: str, payload: dict[str, Any], *, dedupe: bool) -> CommercialNarrativeBlock:
    """Fill one mapped section after machine cleanup and optional meaning merge."""
    lines = clean_lines(lines_for_section(payload, slot))
    if dedupe:
        lines = dedupe_lines(lines)
    return _block(slot, lines)


def _block(slot: str, lines: tuple) -> CommercialNarrativeBlock:
    """Build a commercial section from published lines."""
    sentences = to_sentences(slot, lines)
    if not sentences:
        return empty_commercial_block(slot)
    return CommercialNarrativeBlock(
        slot=slot,
        sentences=sentences,
        available=True,
        insufficient=False,
    )


def _status(blocks: dict[str, CommercialNarrativeBlock]) -> str:
    """Customer-facing completeness follows frozen INT-03B section order."""
    if not blocks["current_situation"].available:
        return "insufficient"
    if all(blocks[slot].available for slot in CUSTOMER_SECTION_ORDER):
        return "complete"
    return "partial"
