"""Recommendation builder — copy published Pattern / Useful God / Temperature guidance only."""

from __future__ import annotations

from typing import Any

from engines.narrative_framework.pattern.blocks import make_block
from engines.narrative_framework.pattern.evidence import _payload
from engines.narrative_framework.pattern.models import PatternEvidence, PatternNarrativeBlock


def _text(data: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = data.get(key)
        if value is None or value == "":
            continue
        if isinstance(value, (list, tuple)):
            joined = " · ".join(str(item).strip() for item in value if str(item).strip())
            if joined:
                return joined
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


def build_recommendation(
    evidence: PatternEvidence,
    useful_god: Any = None,
    temperature: Any = None,
) -> PatternNarrativeBlock:
    """Restate published Pattern / Useful God / Temperature guidance. No new advice."""
    sentences: list[str] = []
    paths: list[str] = []
    god = _payload(useful_god)
    temp = _payload(temperature)
    useful = _text(god, "useful_display", "dung_than", "useful_god") or evidence.dung_than
    if useful:
        sentences.append(f"Ưu tiên hướng Dụng thần đã công bố: {useful}.")
        paths.append("useful_god" if god else "pattern.dung_than")
    favorable = _text(god, "canonical_favorable_display", "favorable_display") or evidence.hy_than
    if favorable:
        sentences.append(f"Hỷ thần đã công bố: {favorable}.")
        paths.append("useful_god.favorable" if god else "pattern.hy_than")
    unfavorable = _text(god, "unfavorable_display") or evidence.ky_than
    if unfavorable:
        sentences.append(f"Hạn chế Kỵ thần đã công bố: {unfavorable}.")
        paths.append("useful_god.unfavorable" if god else "pattern.ky_than")
    climate = _text(
        temp,
        "balancing_need_label",
        "balancing_need",
        "climate_state_label",
    ) or evidence.dieu_hau
    if climate:
        sentences.append(f"Hướng điều hậu đã công bố: {climate}.")
        paths.append("temperature" if temp else "pattern.dieu_hau")
    published_recs = temp.get("recommendations") if isinstance(temp.get("recommendations"), list) else []
    for item in (*evidence.recommendations, *published_recs):
        text = str(item).strip()
        if not text:
            continue
        sentences.append(text if text.endswith(".") else text + ".")
        paths.append("pattern.recommendations")
    return make_block("recommendation", tuple(sentences), tuple(paths))
