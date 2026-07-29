"""
Portal-facing InterpretationView serialization.

Sole producer of the commercial ``sections[]`` JSON shape used by
AnalysisResult.interpretation / Portal. Internal rule IDs stay off the wire.
"""

from __future__ import annotations

import re
from typing import Any

SECTION_TITLES: dict[str, str] = {
    "summary": "Tổng quan",
    "strength": "Điểm mạnh",
    "weakness": "Điểm cần lưu ý",
    "warning": "Lưu ý",
    "career": "Sự nghiệp",
    "wealth": "Tài vận",
    "relationship": "Quan hệ",
    "health": "Sức khỏe",
    "personality": "Tính cách",
    "luck": "Đại vận",
    "useful_god": "Dụng thần",
    "pattern": "Cách cục",
    "conclusion": "Kết luận",
    "children": "Con cái",
    "yearly_fortune": "Lưu niên",
}

SECTION_ORDER: tuple[str, ...] = (
    "summary",
    "personality",
    "career",
    "wealth",
    "relationship",
    "health",
    "useful_god",
    "luck",
    "pattern",
    "conclusion",
    "warning",
    "strength",
    "weakness",
)

_INTERNAL_LINE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\b(?:FPR|SPR|PAT|PSC|PPR|SER|SDR|CBR|PC)\d+\b"),
    re.compile(
        r"\b(?:rule id|internal code|json key|metadata|template schema|debug text)\b",
        re.I,
    ),
    re.compile(r"\bupstream\b", re.I),
    re.compile(r"\bstatus\s*=", re.I),
    re.compile(r"\bDa kich hoat cac nhom luan giai\b", re.I),
    re.compile(r"\bBTE Report Template Schema\b", re.I),
)

# Raw unaccented Latin tokens (humanize_token rule names), e.g. "Kiep Tai Cach".
_RAW_RULE_LINE_RE = re.compile(r"^[A-Za-z][A-Za-z0-9 _\-/()]*$")


def humanize_token(value: str) -> str:
    """Convert snake-like tokens into readable labels."""
    text = str(value or "").strip()
    if not text:
        return ""
    if re.fullmatch(r"[a-z0-9_]+", text):
        return " ".join(part.capitalize() for part in text.split("_") if part)
    return text


def is_internal_text(text: str) -> bool:
    """Return True when a sentence/line is internal or debug-oriented."""
    raw = str(text or "").strip()
    if not raw:
        return True
    if _RAW_RULE_LINE_RE.fullmatch(raw):
        return True
    return any(pattern.search(raw) for pattern in _INTERNAL_LINE_PATTERNS)


def sanitize_sentence(text: str) -> str:
    """Remove internal markers while preserving user-facing prose."""
    cleaned = str(text or "").strip()
    if not cleaned or is_internal_text(cleaned):
        return ""
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(
        r"\b([a-z]+(?:_[a-z0-9]+)+)\b",
        lambda match: humanize_token(match.group(1)),
        cleaned,
    )
    return cleaned.strip()


def build_portal_dict(result: Any) -> dict[str, Any]:
    """
    Build portal-compatible InterpretationView from InterpretationResult.

    Production response exposes only commercial fields:
    sections, section_count, sentence_count, confidence.

    Internal engine fields stay off the wire:
    summary, matched_rule_count, resolved_rule_count, coverage,
    metadata, priority_resolution, discarded_rules, unused_rules.
    """
    grouped: dict[str, list[str]] = {}
    for item in getattr(result, "sentences", None) or []:
        if not isinstance(item, dict):
            continue
        section = str(item.get("section") or "").strip().lower()
        sentence = sanitize_sentence(str(item.get("sentence") or ""))
        if not section or not sentence:
            continue
        grouped.setdefault(section, []).append(sentence)

    sections: list[dict[str, str]] = []
    for key in SECTION_ORDER:
        lines = grouped.get(key) or []
        if not lines:
            continue
        deduped = list(dict.fromkeys(lines))
        sections.append(
            {
                "id": key,
                "title": SECTION_TITLES.get(key, humanize_token(key)),
                "body": "\n\n".join(deduped),
            }
        )

    confidence = getattr(result, "confidence", 0) or 0
    try:
        confidence_value = float(confidence)
    except (TypeError, ValueError):
        confidence_value = 0.0

    sentence_count = sum(
        len(section["body"].split("\n\n")) for section in sections
    )
    return {
        "sections": sections,
        "section_count": len(sections),
        "sentence_count": sentence_count,
        "confidence": confidence_value,
    }
