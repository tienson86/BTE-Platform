"""Summary builder — synthesizes prior blocks. No new facts."""

from __future__ import annotations

from engines.narrative_framework.pattern.blocks import make_block
from engines.narrative_framework.pattern.models import PatternNarrativeBlock


def _first_sentence(block: PatternNarrativeBlock) -> str | None:
    if not block.available or not block.sentences:
        return None
    text = block.sentences[0].strip()
    return text or None


def build_summary(
    observation: PatternNarrativeBlock,
    reasoning: PatternNarrativeBlock,
    impact: PatternNarrativeBlock,
    recommendation: PatternNarrativeBlock,
) -> PatternNarrativeBlock:
    """Join the first sentence of each prior block. Introduce no new facts."""
    parts: list[str] = []
    paths: list[str] = []
    for block, path in (
        (observation, "pattern.narrative.observation"),
        (reasoning, "pattern.narrative.reasoning"),
        (impact, "pattern.narrative.impact"),
        (recommendation, "pattern.narrative.recommendation"),
    ):
        sentence = _first_sentence(block)
        if sentence:
            parts.append(sentence.rstrip("."))
            paths.append(path)
    if not parts:
        return make_block("summary", (), ())
    summary = ". ".join(parts) + "."
    return make_block("summary", (summary,), tuple(paths))
