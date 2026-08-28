"""Observation builder — classified Luck evidence."""

from __future__ import annotations

from engines.narrative_framework.luck.blocks import make_block
from engines.narrative_framework.luck.classify import classify_luck_evidence
from engines.narrative_framework.luck.models import (
    LuckEvidence,
    LuckNarrativeBlock,
    LuckNarrativeEvidencePack,
)


def _pack(
    source: LuckEvidence | LuckNarrativeEvidencePack,
) -> LuckNarrativeEvidencePack:
    if isinstance(source, LuckNarrativeEvidencePack):
        return source
    return classify_luck_evidence(source)


def build_observation(
    source: LuckEvidence | LuckNarrativeEvidencePack,
) -> LuckNarrativeBlock:
    """Name published Đại Vận, Lưu Niên, and timeline. It does not advise."""
    pack = _pack(source)
    sentences: list[str] = []
    paths: list[str] = []
    cycle = pack.item("current_cycle")
    if cycle and cycle.display_value:
        sentences.append(f"Đại Vận hiện tại đã công bố là {cycle.display_value}.")
        paths.append(cycle.source_path)
    liunian = pack.item("current_liunian")
    if liunian and liunian.display_value:
        sentences.append(f"Lưu Niên hiện tại đã công bố là {liunian.display_value}.")
        paths.append(liunian.source_path)
    timeline = pack.item("timeline")
    if timeline and timeline.display_value:
        sentences.append(f"Timeline đã công bố là {timeline.display_value}.")
        paths.append(timeline.source_path)
    return make_block("observation", tuple(sentences), tuple(paths))
