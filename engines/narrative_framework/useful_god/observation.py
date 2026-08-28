"""Observation builder — classified Useful God evidence."""

from __future__ import annotations

from engines.narrative_framework.useful_god.blocks import make_block
from engines.narrative_framework.useful_god.classify import classify_useful_god_evidence
from engines.narrative_framework.useful_god.models import (
    UsefulGodEvidence,
    UsefulGodNarrativeBlock,
    UsefulGodNarrativeEvidencePack,
)


def _pack(
    source: UsefulGodEvidence | UsefulGodNarrativeEvidencePack,
) -> UsefulGodNarrativeEvidencePack:
    if isinstance(source, UsefulGodNarrativeEvidencePack):
        return source
    return classify_useful_god_evidence(source)


def build_observation(
    source: UsefulGodEvidence | UsefulGodNarrativeEvidencePack,
) -> UsefulGodNarrativeBlock:
    """Name the published Useful God. It does not advise."""
    pack = _pack(source)
    sentences: list[str] = []
    paths: list[str] = []
    target = pack.item("useful_god")
    if target and target.display_value:
        sentences.append(f"Dụng thần đã công bố là {target.display_value}.")
        paths.append(target.source_path)
    ten_god = pack.raw_evidence.useful_ten_god
    if ten_god:
        sentences.append(f"Thập thần Dụng thần đã công bố là {ten_god}.")
        paths.append("useful_god.useful_ten_god")
    return make_block("observation", tuple(sentences), tuple(paths))
