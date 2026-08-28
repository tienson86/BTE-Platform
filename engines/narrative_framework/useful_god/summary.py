"""Summary builder — synthesizes prior blocks. No new facts."""

from __future__ import annotations

from engines.narrative_framework.useful_god.blocks import make_block
from engines.narrative_framework.useful_god.models import UsefulGodNarrativeBlock


def _first_sentence(block: UsefulGodNarrativeBlock) -> str | None:
    if not block.available or not block.sentences:
        return None
    text = block.sentences[0].strip()
    return text or None


def build_summary(
    observation: UsefulGodNarrativeBlock,
    reasoning: UsefulGodNarrativeBlock,
    impact: UsefulGodNarrativeBlock,
    recommendation: UsefulGodNarrativeBlock,
) -> UsefulGodNarrativeBlock:
    """Join the first sentence of each prior block. Introduce no new facts."""
    parts: list[str] = []
    paths: list[str] = []
    for block, path in (
        (observation, "useful_god.narrative.observation"),
        (reasoning, "useful_god.narrative.reasoning"),
        (impact, "useful_god.narrative.impact"),
        (recommendation, "useful_god.narrative.recommendation"),
    ):
        sentence = _first_sentence(block)
        if sentence:
            parts.append(sentence.rstrip("."))
            paths.append(path)
    if not parts:
        return make_block("summary", (), ())
    summary = ". ".join(parts) + "."
    return make_block("summary", (summary,), tuple(paths))
