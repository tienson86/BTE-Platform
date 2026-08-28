"""Observation builder — classified Pattern evidence."""

from __future__ import annotations

from engines.narrative_framework.pattern.blocks import make_block
from engines.narrative_framework.pattern.classify import classify_pattern_evidence
from engines.narrative_framework.pattern.models import (
    PatternEvidence,
    PatternNarrativeBlock,
    PatternNarrativeEvidencePack,
)


def _pack(
    source: PatternEvidence | PatternNarrativeEvidencePack,
) -> PatternNarrativeEvidencePack:
    if isinstance(source, PatternNarrativeEvidencePack):
        return source
    return classify_pattern_evidence(source)


def build_observation(
    source: PatternEvidence | PatternNarrativeEvidencePack,
) -> PatternNarrativeBlock:
    """Name the published Pattern, Điều hậu, and special pattern. It does not advise."""
    pack = _pack(source)
    sentences: list[str] = []
    paths: list[str] = []
    pattern = pack.item("pattern")
    if pattern and pattern.display_value:
        sentences.append(f"Cách cục đã công bố là {pattern.display_value}.")
        paths.append(pattern.source_path)
    dieu_hau = pack.item("dieu_hau")
    if dieu_hau and dieu_hau.display_value:
        sentences.append(f"Điều hậu đã công bố là {dieu_hau.display_value}.")
        paths.append(dieu_hau.source_path)
    special = pack.item("special_pattern")
    if special and special.display_value:
        sentences.append(f"Cấu trúc đặc biệt đã công bố là {special.display_value}.")
        paths.append(special.source_path)
    return make_block("observation", tuple(sentences), tuple(paths))
