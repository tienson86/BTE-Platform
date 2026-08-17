"""Current Da Yun consultation for Professional edition.

Assembles already-composed natal narrative with already-copied cycle labels.
Does not calculate luck, interpret all ten cycles, or add a Luck Domain.
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
from engines.interpretation_engine.foundation.narrative.text import normalize_text

_GLOSSARY_MARKERS: tuple[str, ...] = (
    "đại vận là",
    "mười đại vận",
    "lý thuyết đại vận",
    "cách tính đại vận",
    "encyclopedia",
)

_LEAD_PREFIXES: tuple[str, ...] = (
    "tóm tắt điều hành",
    "quan sát",
    "lý giải",
    "tác động",
    "khuyến nghị",
    "lưu ý",
    "kết luận",
    "sự nghiệp:",
    "tài chính:",
    "quan hệ:",
    "sức khỏe:",
)

_REC_LEAD = re.compile(
    r"^(?:\d+\.\s*)?(?:làm|tránh|xây|củng cố|giảm|dùng)\s*:\s*",
    re.IGNORECASE,
)


def assemble_current_dayun_consultation(
    payload: dict[str, Any],
    published: dict[str, list[str]],
    *,
    exclude: list[str],
) -> list[str]:
    """Build the Professional Current Da Yun page from existing truth only."""
    current = _current_label(payload, published)
    if not current:
        return []
    thesis = _thesis(payload)
    hy_gods = _field_from_observation(published, "Hỷ thần:")
    ky_gods = _field_from_observation(published, "Kỵ thần:")
    useful = _field_from_observation(published, "Dụng thần được chọn:")
    paragraphs = [
        _decade_paragraph(current),
        _why_paragraph(current, thesis, published),
        _interaction_paragraph(current, thesis, published, useful, hy_gods, ky_gods),
        _opportunity_paragraph(current, thesis, published),
        _risk_paragraph(current, thesis, published),
        _direction_paragraph(current, thesis, published),
        _next_paragraph(current, _next_label(payload)),
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


def _decade_paragraph(current: str) -> str:
    """Name the living decade. Not a glossary of Da Yun theory."""
    return (
        f"Đại vận đang sống là {current}. "
        "Đây là thập niên cần luận cho khách hàng, không phải toàn bộ chuỗi đại vận."
    )


def _why_paragraph(
    current: str,
    thesis: dict[str, Any],
    published: dict[str, list[str]],
) -> str:
    """Why this decade matters for this chart, using the existing thesis."""
    title = str(thesis.get("title") or "").strip()
    body = str(thesis.get("short_thesis") or thesis.get("expanded_thesis") or "").strip()
    if not body:
        body = _first_consulting(published.get("sec-executive_summary") or [], current)
    if title and body:
        return (
            f"{current} quan trọng vì đây là thập niên {title} phải giữ hướng đã luận: {body}"
        )
    if body:
        return f"{current} quan trọng vì {body}"
    return ""


def _interaction_paragraph(
    current: str,
    thesis: dict[str, Any],
    published: dict[str, list[str]],
    useful: str,
    hy_gods: str,
    ky_gods: str,
) -> str:
    """Natal Pattern / Strength / Useful God / Hỷ / Kỵ during this decade."""
    pattern = str(thesis.get("core_pattern") or "").strip()
    strength = str(thesis.get("core_strength") or "").strip()
    corrective = str(thesis.get("corrective_direction") or "").strip()
    parts = [f"Trong {current}, lá số vẫn vận hành trên cấu trúc đã luận"]
    if pattern:
        parts.append(f"nền {pattern}")
    if strength:
        parts.append(strength)
    if useful:
        parts.append(f"trục Dụng {useful}")
    sentence = ", ".join(parts) + "."
    if corrective:
        sentence = f"{sentence} Hướng chỉnh vẫn là {corrective}."
    if hy_gods:
        sentence = f"{sentence} Hỷ thần hiện có: {hy_gods}."
    if ky_gods:
        sentence = f"{sentence} Kỵ thần hiện có: {ky_gods}."
    reasoning = _first_consulting(published.get("sec-reasoning") or [], current)
    if reasoning and word_count(reasoning) >= MIN_CONSULTING_WORDS:
        sentence = f"{sentence} {reasoning}"
    return sentence


def _opportunity_paragraph(
    current: str,
    thesis: dict[str, Any],
    published: dict[str, list[str]],
) -> str:
    """Main opportunity copied from capacities, career implication, or first rec."""
    rec = _first_action(published.get("sec-recommendation") or [])
    career = str(thesis.get("career_implication") or "").strip()
    capacities = thesis.get("primary_capacities") or []
    capacity = str(capacities[0]).strip() if capacities else ""
    body = career or rec or capacity
    if not body:
        return ""
    return f"Cơ hội chính trong {current}: {body}"


def _risk_paragraph(
    current: str,
    thesis: dict[str, Any],
    published: dict[str, list[str]],
) -> str:
    """Main pressure copied from thesis risk or an existing warning."""
    risks = thesis.get("primary_risks") or []
    risk = str(risks[0]).strip() if risks else ""
    tension = str(thesis.get("core_tension") or "").strip()
    warning = _first_consulting(published.get("sec-warning") or [], current)
    body = risk or tension or warning
    if not body:
        return ""
    return f"Áp lực chính trong {current}: {body}"


def _direction_paragraph(
    current: str,
    thesis: dict[str, Any],
    published: dict[str, list[str]],
) -> str:
    """How to operate in this decade, from corrective direction and first action."""
    corrective = str(thesis.get("corrective_direction") or "").strip()
    career = str(thesis.get("career_implication") or "").strip()
    rec = _first_action(published.get("sec-recommendation") or [])
    parts: list[str] = []
    if corrective:
        parts.append(corrective.rstrip("."))
    follow = career or rec
    if follow and follow.rstrip(".").casefold() not in " ".join(parts).casefold():
        parts.append(follow.rstrip("."))
    if not parts:
        return ""
    return f"Hướng vận hành nên giữ trong {current}: {'. '.join(parts)}."


def _next_paragraph(current: str, nxt: str) -> str:
    """Name the next cycle briefly. Do not interpret all ten cycles."""
    if not nxt or nxt == current:
        return (
            f"Không luận toàn bộ mười đại vận. Giữ hướng đã chọn đến hết {current}."
        )
    return (
        f"Đại vận kế tiếp đã có trên lá số là {nxt}; đó chưa phải thập niên đang sống. "
        f"Không luận mười vòng. Giữ hướng hiện tại đến hết {current}."
    )


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


def _next_label(payload: dict[str, Any]) -> str:
    """Read the copied next cycle label when present."""
    return str(_frame(payload).get("next_dayun") or "").strip()


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


def _thesis(payload: dict[str, Any]) -> dict[str, Any]:
    """Case thesis already attached by the composer."""
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        return {}
    thesis = metadata.get("case_thesis")
    return thesis if isinstance(thesis, dict) else {}


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


def _first_action(texts: list[str]) -> str:
    """First recommendation without list chrome."""
    for text in texts:
        blob = _strip_lead(text)
        blob = _REC_LEAD.sub("", blob).strip()
        if word_count(blob) >= 4:
            return blob
    return ""


def _first_consulting(texts: list[str], current: str) -> str:
    """First already-composed consulting sentence that is not a luck timestamp."""
    for text in texts:
        blob = _strip_lead(text)
        if not blob:
            continue
        if _is_timestamp_only(blob, current):
            continue
        if any(marker in blob.casefold() for marker in _GLOSSARY_MARKERS):
            continue
        if word_count(blob) >= MIN_CONSULTING_WORDS:
            return blob
    return ""


def _is_timestamp_only(text: str, current: str) -> bool:
    """True when the sentence only names the cycle."""
    lowered = text.casefold()
    if current and current.casefold() in lowered and word_count(text) <= 14:
        return True
    return lowered.startswith("khung thời gian") or lowered.startswith("đại vận hiện tại:")


def _strip_lead(text: str) -> str:
    """Remove section chrome copied from published paragraphs."""
    blob = normalize_text(text)
    lowered = blob.casefold()
    for prefix in _LEAD_PREFIXES:
        if lowered.startswith(prefix):
            blob = blob[len(prefix) :].strip(" :.")
            lowered = blob.casefold()
    return blob


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
