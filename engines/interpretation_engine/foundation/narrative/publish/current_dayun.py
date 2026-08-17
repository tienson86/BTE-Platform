"""Current Da Yun consultation for Professional edition.

Consumes stamped Luck Analysis Facts. Does not calculate luck, interpret all
ten cycles, or paste natal thesis onto the decade name.
"""

from __future__ import annotations

import re
from typing import Any

from engines.interpretation_engine.foundation.narrative.publish.criteria import (
    word_count,
)
from engines.interpretation_engine.foundation.narrative.publish.editions import (
    MIN_CONSULTING_WORDS,
    PROFESSIONAL_SECTION_LIMITS,
)
from engines.interpretation_engine.foundation.narrative.publish.luck_analysis_copy import (
    luck_analysis_from_payload,
    luck_paragraphs_from_analysis,
)
from engines.interpretation_engine.foundation.narrative.text import normalize_text

_GLOSSARY_MARKERS: tuple[str, ...] = (
    "đại vận là",
    "mười đại vận",
    "lý thuyết đại vận",
    "cách tính đại vận",
    "encyclopedia",
)


def assemble_current_dayun_consultation(
    payload: dict[str, Any],
    published: dict[str, list[str]],
    *,
    exclude: list[str],
) -> list[str]:
    """Build the Professional Current Da Yun page from Luck Analysis Facts only."""
    data = luck_analysis_from_payload(payload)
    paragraphs = luck_paragraphs_from_analysis(data)
    if not paragraphs:
        current = _current_label(payload, published)
        if current:
            paragraphs = [
                (
                    f"Đại vận đang sống là {current}. "
                    "Phân tích production hiện tại chưa xác định thêm tương tác "
                    "ngoài luận giải gốc. Không lặp luận giải gốc."
                )
            ]
    return _unique_kept(paragraphs, exclude, PROFESSIONAL_SECTION_LIMITS["sec-luck"])


def stamp_dayun_frame(payload: dict[str, Any], engine_output: Any) -> dict[str, Any]:
    """Copy current/next cycle labels onto the payload. Do not interpret them."""
    from engines.interpretation_engine.foundation.narrative.production import (
        dayun_frame_from_production,
    )

    if not isinstance(payload, dict) or engine_output is None:
        return payload
    frame = dayun_frame_from_production(engine_output)
    if not frame.get("current_dayun"):
        return payload
    out = dict(payload)
    metadata = dict(out.get("metadata") or {}) if isinstance(out.get("metadata"), dict) else {}
    metadata["luck_frame"] = frame
    out["metadata"] = metadata
    return out


def stamp_luck_analysis(payload: dict[str, Any], engine_output: Any) -> dict[str, Any]:
    """Copy Luck Analysis facts onto narrative metadata. Do not calculate them."""
    if not isinstance(payload, dict) or engine_output is None:
        return payload
    foundation = getattr(engine_output, "interpretation_foundation", None)
    analysis = getattr(foundation, "luck_analysis", None) if foundation is not None else None
    if analysis is None or not hasattr(analysis, "to_dict"):
        return payload
    out = dict(payload)
    metadata = dict(out.get("metadata") or {}) if isinstance(out.get("metadata"), dict) else {}
    metadata["luck_analysis"] = analysis.to_dict()
    out["metadata"] = metadata
    return out


def stamp_interaction_truth(payload: dict[str, Any], engine_output: Any) -> dict[str, Any]:
    """Copy Interaction Truth facts onto narrative metadata. Do not calculate them."""
    if not isinstance(payload, dict) or engine_output is None:
        return payload
    foundation = getattr(engine_output, "interpretation_foundation", None)
    interaction = getattr(foundation, "interaction_truth", None) if foundation is not None else None
    if interaction is None or not hasattr(interaction, "to_dict"):
        return payload
    out = dict(payload)
    metadata = dict(out.get("metadata") or {}) if isinstance(out.get("metadata"), dict) else {}
    metadata["interaction_truth"] = interaction.to_dict()
    out["metadata"] = metadata
    return out


def _current_label(payload: dict[str, Any], published: dict[str, list[str]]) -> str:
    """Read the copied current cycle label."""
    frame = _frame(payload)
    if frame.get("current_dayun"):
        return frame["current_dayun"]
    observed = _field_from_observation(published, "Đại vận hiện tại:")
    if observed:
        return observed
    for text in published.get("sec-executive_summary") or []:
        match = re.search(r"Đại vận\s+(.+?)\.?\s*$", text)
        if match:
            return normalize_text(match.group(1))
    return ""


def _frame(payload: dict[str, Any]) -> dict[str, str]:
    """Luck labels stamped from production. Empty when missing."""
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        return {}
    raw = metadata.get("luck_frame")
    if not isinstance(raw, dict):
        return {}
    return {
        "current_dayun": str(raw.get("current_dayun") or "").strip(),
        "next_dayun": str(raw.get("next_dayun") or "").strip(),
    }


def _field_from_observation(published: dict[str, list[str]], prefix: str) -> str:
    """Copy one observation fact after its label."""
    needle = prefix.casefold()
    for text in published.get("sec-observation") or []:
        blob = normalize_text(text)
        lowered = blob.casefold()
        if needle not in lowered:
            continue
        start = lowered.find(needle)
        rest = blob[start + len(prefix) :].strip()
        rest = rest.split(".")[0].strip()
        rest = re.split(r"\s{2,}|Thân |Cục:", rest)[0].strip(" .;")
        if rest:
            return rest
    return ""


def _unique_kept(texts: list[str], exclude: list[str], limit: int) -> list[str]:
    """Drop empty, glossary, and duplicate paragraphs."""
    kept: list[str] = []
    blocked = [normalize_text(item) for item in exclude]
    for text in texts:
        blob = normalize_text(text)
        if word_count(blob) < MIN_CONSULTING_WORDS:
            continue
        if any(marker in blob.casefold() for marker in _GLOSSARY_MARKERS):
            continue
        if blob in blocked:
            continue
        kept.append(blob)
        blocked.append(blob)
        if len(kept) >= limit:
            break
    return kept
