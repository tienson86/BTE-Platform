"""Reasoning builder — grouped classified Luck evidence. No rescoring."""

from __future__ import annotations

from engines.narrative_framework.luck.blocks import make_block
from engines.narrative_framework.luck.classify import classify_luck_evidence
from engines.narrative_framework.luck.constants import (
    PUBLISHED_CLASS_PREFIX,
    RESTRAIN_GROUP_LABEL,
    SUPPORT_GROUP_LABEL,
)
from engines.narrative_framework.luck.models import (
    LuckEvidence,
    LuckNarrativeBlock,
    LuckNarrativeEvidencePack,
)

_DIRECTIONAL = frozenset({"support", "attack"})


def _pack(
    source: LuckEvidence | LuckNarrativeEvidencePack,
) -> LuckNarrativeEvidencePack:
    if isinstance(source, LuckNarrativeEvidencePack):
        return source
    return classify_luck_evidence(source)


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
    source: LuckEvidence | LuckNarrativeEvidencePack,
) -> LuckNarrativeBlock:
    """Explain the published Luck reading from timeline and classified evidence."""
    pack = _pack(source)
    evidence = pack.raw_evidence
    sentences: list[str] = []
    paths: list[str] = []
    if evidence.reasoning:
        sentences.append(evidence.reasoning.rstrip(".") + ".")
        paths.append("luck.luck_summary")
    if evidence.timeline:
        sentences.append(f"Timeline đã công bố: {evidence.timeline}.")
        paths.append("luck.timeline")
    support_line = _group_line(SUPPORT_GROUP_LABEL, pack.positive_evidence)
    if support_line:
        sentences.append(support_line)
        paths.append("luck.evidence_pack.positive")
    restrain_line = _group_line(RESTRAIN_GROUP_LABEL, pack.negative_evidence)
    if restrain_line:
        sentences.append(restrain_line)
        paths.append("luck.evidence_pack.negative")
    stage = evidence.luck_stage or evidence.current_cycle
    if stage:
        sentences.append(f"{PUBLISHED_CLASS_PREFIX} {stage}.")
        paths.append("luck.luck_stage" if evidence.luck_stage else "luck.current_dayun")
    return make_block("reasoning", tuple(sentences), tuple(paths))
