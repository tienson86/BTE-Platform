"""Recommendation builder — copy published Useful God / Temperature guidance only."""

from __future__ import annotations

from typing import Any, Mapping

from engines.narrative_framework.strength.blocks import make_block
from engines.narrative_framework.strength.evidence import _payload
from engines.narrative_framework.strength.models import StrengthEvidence, StrengthNarrativeBlock


def _text(data: Mapping[str, Any], *keys: str) -> str:
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
    evidence: StrengthEvidence,
    useful_god: Any = None,
    temperature: Any = None,
) -> StrengthNarrativeBlock:
    """Restate published Useful God and Temperature guidance. No new advice."""
    sentences: list[str] = []
    paths: list[str] = []
    god = _payload(useful_god)
    temp = _payload(temperature)
    useful = _text(god, "useful_display", "dung_than", "useful_god", "useful_element")
    if useful:
        sentences.append(f"Ưu tiên hướng Dụng thần đã công bố: {useful}.")
        paths.append("useful_god")
    favorable = _text(god, "canonical_favorable_display", "favorable_display", "favorable_gods")
    if favorable:
        sentences.append(f"Hỷ thần đã công bố: {favorable}.")
        paths.append("useful_god.favorable")
    climate = _text(
        temp,
        "balancing_need_label",
        "balancing_need",
        "climate_state_label",
        "climate_state",
        "temperature_level",
    )
    if climate:
        sentences.append(f"Hướng điều hậu đã công bố: {climate}.")
        paths.append("temperature")
    published_recs = temp.get("recommendations") if isinstance(temp.get("recommendations"), list) else []
    for item in published_recs:
        text = str(item).strip()
        if text:
            sentences.append(text if text.endswith(".") else text + ".")
            paths.append("temperature.recommendations")
    if evidence.temperature_state and not climate:
        sentences.append(f"Trạng thái điều hậu đã công bố: {evidence.temperature_state}.")
        paths.append("temperature.temperature_state")
    return make_block("recommendation", tuple(sentences), tuple(paths))
