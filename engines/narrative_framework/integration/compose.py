"""Assemble IntegratedNarrativeUnit from frozen topic narrative units."""

from __future__ import annotations

from typing import Any

from engines.narrative_framework.integration.constants import INTEGRATED_BLOCKS
from engines.narrative_framework.integration.merge import (
    MergedLine,
    drop_used,
    executive_lines,
    merge_topics,
    ordered_units,
)
from engines.narrative_framework.integration.models import (
    IntegratedNarrativeBlock,
    IntegratedNarrativeUnit,
)


def make_block(slot: str, lines: tuple[MergedLine, ...]) -> IntegratedNarrativeBlock:
    """Build a present or insufficient integrated block."""
    ready = bool(lines)
    return IntegratedNarrativeBlock(
        slot=slot,
        sentences=tuple(line[0] for line in lines),
        source_paths=tuple(line[1] for line in lines) if ready else (),
        topic_ids=tuple(line[2] for line in lines) if ready else (),
        available=ready,
        insufficient=not ready,
    )


def _summary_lines(
    observation: IntegratedNarrativeBlock,
    reasoning: IntegratedNarrativeBlock,
    impact: IntegratedNarrativeBlock,
    recommendation: IntegratedNarrativeBlock,
) -> tuple[MergedLine, ...]:
    parts: list[MergedLine] = []
    for block, path in (
        (observation, "integrated.observation"),
        (reasoning, "integrated.reasoning"),
        (impact, "integrated.impact"),
        (recommendation, "integrated.recommendation"),
    ):
        if not block.available or not block.sentences:
            continue
        text = block.sentences[0].strip().rstrip(".")
        topic = block.topic_ids[0] if block.topic_ids else ""
        parts.append((text, path, topic))
    if not parts:
        return ()
    joined = ". ".join(line[0] for line in parts) + "."
    topics = tuple(line[2] for line in parts if line[2])
    paths = tuple(line[1] for line in parts)
    return ((joined, paths[0] if paths else "integrated.summary", topics[0] if topics else ""),)


def _lines_of(block: IntegratedNarrativeBlock) -> tuple[MergedLine, ...]:
    return tuple(
        (block.sentences[index], block.source_paths[index], block.topic_ids[index])
        for index in range(len(block.sentences))
    )


def _status(observation_ok: bool, others_ok: tuple[bool, ...]) -> str:
    if not observation_ok:
        return "insufficient"
    if all(others_ok):
        return "complete"
    return "partial"


def compose_integrated_narrative(
    strength: Any = None,
    useful_god: Any = None,
    pattern: Any = None,
    luck: Any = None,
) -> IntegratedNarrativeUnit:
    """Merge → Deduplicate → Executive Summary → five speech blocks."""
    units = ordered_units(strength, useful_god, pattern, luck)
    merged = merge_topics(units)
    exec_lines = executive_lines(units)
    observation = make_block(
        "observation",
        drop_used(merged["observation"], exec_lines, restatement=True),
    )
    prior = exec_lines + _lines_of(observation)
    reasoning = make_block(
        "reasoning",
        drop_used(merged["reasoning"], prior, restatement=True),
    )
    prior = prior + _lines_of(reasoning)
    impact = make_block(
        "impact",
        drop_used(merged["impact"], prior, restatement=True),
    )
    recommendation = make_block("recommendation", merged["recommendation"])
    executive = make_block("executive_summary", exec_lines)
    summary = make_block(
        "summary",
        _summary_lines(observation, reasoning, impact, recommendation),
    )
    refs = tuple(
        path
        for block in (executive, observation, reasoning, impact, recommendation, summary)
        for path in block.source_paths
    )
    observation_ok = observation.available or executive.available
    return IntegratedNarrativeUnit(
        executive_summary=executive,
        observation=observation,
        reasoning=reasoning,
        impact=impact,
        recommendation=recommendation,
        summary=summary,
        topics=tuple(str(getattr(unit, "topic_id", "")) for unit in units),
        status=_status(
            observation_ok,
            (
                reasoning.available,
                impact.available,
                recommendation.available,
                summary.available,
            ),
        ),
        evidence_refs=refs,
    )


def integrated_block_order() -> tuple[str, ...]:
    """Public block order for consumers."""
    return INTEGRATED_BLOCKS
