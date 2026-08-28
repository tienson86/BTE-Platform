"""Summary builder — synthesizes prior blocks. No new facts."""

from __future__ import annotations

from engines.narrative_framework.luck.blocks import make_block
from engines.narrative_framework.luck.models import LuckNarrativeBlock


def _first_sentence(block: LuckNarrativeBlock) -> str | None:
    if not block.available or not block.sentences:
        return None
    text = block.sentences[0].strip()
    return text or None


def build_summary(
    observation: LuckNarrativeBlock,
    reasoning: LuckNarrativeBlock,
    impact: LuckNarrativeBlock,
    recommendation: LuckNarrativeBlock,
) -> LuckNarrativeBlock:
    """Join the first sentence of each prior block. Introduce no new facts."""
    parts: list[str] = []
    paths: list[str] = []
    for block, path in (
        (observation, "luck.narrative.observation"),
        (reasoning, "luck.narrative.reasoning"),
        (impact, "luck.narrative.impact"),
        (recommendation, "luck.narrative.recommendation"),
    ):
        sentence = _first_sentence(block)
        if sentence:
            parts.append(sentence.rstrip("."))
            paths.append(path)
    if not parts:
        return make_block("summary", (), ())
    summary = ". ".join(parts) + "."
    return make_block("summary", (summary,), tuple(paths))
