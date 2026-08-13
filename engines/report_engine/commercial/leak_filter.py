"""Strip developer / engine / rule language from customer PDF text."""

from __future__ import annotations

import re

_HIDDEN_MARKERS = (
    "CAREER_REPORT_HIDDEN_BY_PRODUCT_CONTEXT",
    "IDENTITY_REPORT_HIDDEN_BY_PRODUCT_CONTEXT",
    "EXECUTIVE_CONSULTING_HIDDEN_BY_PRODUCT_CONTEXT",
    "IDENTITY_REPORT_NOT_AVAILABLE",
    "CAREER_REPORT_NOT_AVAILABLE",
    "EXECUTIVE_CONSULTING_NOT_AVAILABLE",
)

_PHRASE_LEAKS = (
    "áp dụng bảng trạng thái",
    "bảng trạng thái",
    "tính cách phản ánh",
    "luận giải strength",
    "luận giải ten_gods",
    "luận giải pattern",
    "luận giải useful_god",
    "luận giải thập thần",
    "rule_id",
    "matched_rules",
    "reason_codes",
    "narrative_plan",
    "validation_mode",
    "executiveclaimplan",
    "crossdomain",
    "claim_id",
    "theme_id",
    "strength_score",
    "engine_version",
    "knowledge_status",
    "domainstatus",
    "appendix a",
    "golden dataset",
    "runtime",
    "pipeline_stages",
    "report_input",
    "ba engine",
    "three engines",
)

_ID_LEAK = re.compile(
    r"\b("
    r"OPERATING_OUTPUT|OPERATING_SELF_CARRY|OPERATING_STANDARDS|"
    r"BALANCE_DIRECTION|FOLLOW_STRUCTURE|FOLLOW_FRAME|"
    r"CAPACITY_STRONG|CAPACITY_WEAK|CAPACITY_BALANCED|"
    r"TENSION_HOLDER|CONSERVING|STABILIZER|"
    r"THEME_[A-Z0-9_]+|RULE[_-][A-Z0-9_]+|"
    r"STR_[A-Z0-9_]+|PAT_[A-Z0-9_]+|UG_[A-Z0-9_]+|TG_[A-Z0-9_]+|"
    r"str_body_level|pat_follow_flag|tg_primary|ug_strategy"
    r")\b",
    re.IGNORECASE,
)

_KICH_HOAT = re.compile(r"kích hoạt\b", re.IGNORECASE)


def is_hidden_feature_marker(text: str) -> bool:
    """True when the feature body is a delivery hide/unavailable marker."""
    raw = (text or "").strip()
    return any(marker in raw for marker in _HIDDEN_MARKERS)


def is_feature_available(status: str, body: str) -> bool:
    """Customer chapter is shown only when commercially available."""
    if (status or "").upper() in {"NOT_AVAILABLE", "INSUFFICIENT"}:
        return False
    if is_hidden_feature_marker(body):
        return False
    return bool((body or "").strip())


def sanitize_paragraph(text: str) -> str:
    """Drop a paragraph that leaks engine/developer language."""
    raw = (text or "").strip()
    if not raw:
        return ""
    if any(marker in raw for marker in _HIDDEN_MARKERS):
        return ""
    lowered = raw.lower()
    if any(phrase in lowered for phrase in _PHRASE_LEAKS):
        return ""
    if _ID_LEAK.search(raw):
        return ""
    if _KICH_HOAT.search(raw) and ("rule" in lowered or "engine" in lowered or "bảng" in lowered):
        return ""
    return raw


def sanitize_paragraphs(paragraphs: list[str]) -> list[str]:
    """Sanitize a list of paragraphs."""
    cleaned: list[str] = []
    seen: set[str] = set()
    for item in paragraphs:
        text = sanitize_paragraph(item)
        if not text or text in seen:
            continue
        seen.add(text)
        cleaned.append(text)
    return cleaned
