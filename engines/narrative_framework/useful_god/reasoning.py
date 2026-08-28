"""Reasoning builder — grouped classified Useful God evidence. No rescoring."""

from __future__ import annotations

from engines.narrative_framework.useful_god.blocks import make_block
from engines.narrative_framework.useful_god.classify import classify_useful_god_evidence
from engines.narrative_framework.useful_god.constants import (
    PUBLISHED_CLASS_PREFIX,
    RESTRAIN_GROUP_LABEL,
    SUPPORT_GROUP_LABEL,
)
from engines.narrative_framework.useful_god.models import (
    UsefulGodEvidence,
    UsefulGodNarrativeBlock,
    UsefulGodNarrativeEvidencePack,
)

_DIRECTIONAL = frozenset(
    {
        "favorable",
        "unfavorable",
        "winning_rule",
        "matched_rules",
        "strength_reason",
        "season_reason",
        "temperature_reason",
        "balance_reason",
    }
)


def _pack(
    source: UsefulGodEvidence | UsefulGodNarrativeEvidencePack,
) -> UsefulGodNarrativeEvidencePack:
    if isinstance(source, UsefulGodNarrativeEvidencePack):
        return source
    return classify_useful_god_evidence(source)


def _group_line(label: str, items: tuple) -> str | None:
    reasons = []
    seen: set[str] = set()
    for item in items:
        if item.component not in _DIRECTIONAL:
            continue
        reason = str(item.reason or "").strip()
        if not reason or reason in seen:
            continue
        seen.add(reason)
        reasons.append(reason)
    if not reasons:
        return None
    return f"{label}: " + ", ".join(reasons) + "."


def build_reasoning(
    source: UsefulGodEvidence | UsefulGodNarrativeEvidencePack,
) -> UsefulGodNarrativeBlock:
    """Explain supporting vs restraining published evidence. Class stays engine-owned."""
    pack = _pack(source)
    evidence = pack.raw_evidence
    sentences: list[str] = []
    paths: list[str] = []
    if evidence.reasoning:
        sentences.append(evidence.reasoning.rstrip(".") + ".")
        paths.append("useful_god.reasoning")
    support_line = _group_line(SUPPORT_GROUP_LABEL, pack.positive_evidence)
    if support_line:
        sentences.append(support_line)
        paths.append("useful_god.evidence_pack.positive")
    restrain_line = _group_line(RESTRAIN_GROUP_LABEL, pack.negative_evidence)
    if restrain_line:
        sentences.append(restrain_line)
        paths.append("useful_god.evidence_pack.negative")
    display = evidence.useful_display or evidence.useful_god
    if display:
        sentences.append(f"{PUBLISHED_CLASS_PREFIX} {display}.")
        paths.append("useful_god.useful_display")
    if evidence.climate_reason:
        sentences.append(evidence.climate_reason.rstrip(".") + ".")
        paths.append("useful_god.climate_reason")
    return make_block("reasoning", tuple(sentences), tuple(paths))
