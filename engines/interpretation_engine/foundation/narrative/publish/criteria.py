"""Publish / Drop / Appendix criteria for one narrative node."""

from __future__ import annotations

import re
from typing import Any, Mapping

from engines.interpretation_engine.foundation.narrative.publish.constants import (
    APPENDIX_MARKERS,
    CHART_FACT_PREFIXES,
    DECISION_APPENDIX,
    DECISION_DROP,
    DECISION_PUBLISH,
    DUMP_CHAR_LIMIT,
    ENGINE_PHRASES,
    ENGINE_WORD_PATTERNS,
    ENGLISH_DOMAIN_TAGS,
    GLOSSARY_MARKERS,
    IMPACT_SPINE_LABELS,
    MEANING_TOKEN_MIN,
    MULTI_TOPIC_GLOSSARY_HITS,
    MULTI_TOPIC_GOD_COUNT,
    TEN_GOD_LABELS,
)
from engines.interpretation_engine.foundation.narrative.text import (
    implementation_language_hits,
    is_broken_fragment,
    is_customer_prose,
    normalize_text,
)
from engines.interpretation_engine.foundation.narrative.translation.validator import (
    find_forbidden_terms,
)

_ENGINE_WORD_RE = tuple(
    re.compile(pattern, flags=re.IGNORECASE) for pattern in ENGINE_WORD_PATTERNS
)
_WORD = re.compile(r"[^\W_]{" + str(MEANING_TOKEN_MIN) + r",}", re.UNICODE)
_SENTENCE = re.compile(r"[.!?。]+")
_HYPOTHETICAL_ROLE = re.compile(
    r"Khi\s+([^,.;:]{1,24}?)\s+là\s+(Dụng thần|Hỷ thần|Hỷ|Kỵ thần|Kỵ)\b"
)
_STOPWORDS = frozenset(
    {
        "là",
        "của",
        "và",
        "khi",
        "một",
        "các",
        "cho",
        "với",
        "không",
        "được",
        "trong",
        "này",
        "để",
        "hay",
        "như",
        "có",
        "the",
        "and",
        "for",
    }
)


def classify_node(
    text: str,
    *,
    section_id: str,
    thesis: Mapping[str, Any] | None,
    chart_names: frozenset[str],
) -> tuple[str, str]:
    """Return (PUBLISH|DROP|APPENDIX, reason). Never a partial publish."""
    blob = normalize_text(text)
    if not blob:
        return DECISION_DROP, "empty"
    if is_broken_fragment(blob) or not is_customer_prose(blob):
        return DECISION_DROP, "not_customer_prose"
    if engine_language_hits(blob):
        return DECISION_DROP, "engine_language"
    if is_english_domain_dump(blob):
        return DECISION_DROP, "english_domain_dump"
    if is_knowledge_dump(blob):
        return DECISION_DROP, "knowledge_dump"
    if is_hypothetical_unused(blob, chart_names):
        return DECISION_DROP, "hypothetical_unused_god"
    if weakens_thesis(blob, thesis):
        return DECISION_DROP, "weakens_thesis"
    if is_appendix_knowledge(blob, section_id, thesis):
        return DECISION_APPENDIX, "correct_but_unnecessary"
    if supports_consultation(blob, section_id, thesis):
        return DECISION_PUBLISH, "supports_consultation"
    return DECISION_APPENDIX, "not_spine"


def engine_language_hits(text: str) -> tuple[str, ...]:
    """Engine, implementation, or debug fragments that must not publish."""
    blob = normalize_text(text)
    lowered = blob.casefold()
    hits: list[str] = []
    hits.extend(find_forbidden_terms(blob))
    hits.extend(implementation_language_hits(blob))
    for phrase in ENGINE_PHRASES:
        if phrase in lowered:
            hits.append(phrase)
    for pattern in _ENGINE_WORD_RE:
        match = pattern.search(blob)
        if match is not None:
            hits.append(match.group(0))
    return tuple(dict.fromkeys(hits))


def is_english_domain_dump(text: str) -> bool:
    """True when a paragraph is an English topic catalogue."""
    hits = sum(1 for tag in ENGLISH_DOMAIN_TAGS if tag in text)
    return hits >= 2 or any(text.startswith(tag) for tag in ENGLISH_DOMAIN_TAGS)


def is_knowledge_dump(text: str) -> bool:
    """True when one paragraph carries multiple independent knowledge topics."""
    lowered = text.casefold()
    glossary_hits = sum(1 for marker in GLOSSARY_MARKERS if marker in lowered)
    god_hits = sum(1 for name in TEN_GOD_LABELS if name in lowered)
    heading_hits = sum(1 for label in IMPACT_SPINE_LABELS if label in text)
    if glossary_hits >= MULTI_TOPIC_GLOSSARY_HITS:
        return True
    if god_hits >= MULTI_TOPIC_GOD_COUNT and len(text) >= DUMP_CHAR_LIMIT:
        return True
    if heading_hits >= 3:
        return True
    if len(text) >= DUMP_CHAR_LIMIT and glossary_hits >= 1:
        return True
    return False


def is_hypothetical_unused(text: str, chart_names: frozenset[str]) -> bool:
    """True when prose explains a Dụng/Hỷ/Kỵ role that is not on this chart."""
    if not chart_names:
        return False
    for match in _HYPOTHETICAL_ROLE.finditer(text):
        name = match.group(1).strip()
        if name and name not in chart_names:
            return True
    return False


def is_appendix_knowledge(
    text: str,
    section_id: str,
    thesis: Mapping[str, Any] | None,
) -> bool:
    """Correct knowledge that must not occupy the customer spine."""
    lowered = text.casefold()
    if any(marker in lowered for marker in APPENDIX_MARKERS):
        return True
    if section_id in {"sec-reasoning", "sec-observation"}:
        if any(marker in lowered for marker in GLOSSARY_MARKERS):
            if not thesis_overlap(text, thesis):
                return True
    return False


def supports_consultation(
    text: str,
    section_id: str,
    thesis: Mapping[str, Any] | None,
) -> bool:
    """True when the paragraph earns a customer-facing slot."""
    lowered = text.casefold()
    if any(lowered.startswith(prefix) for prefix in CHART_FACT_PREFIXES):
        return True
    if section_id in {
        "sec-executive_summary",
        "sec-recommendation",
        "sec-warning",
        "sec-conclusion",
        "sec-impact",
    }:
        return True
    if thesis_overlap(text, thesis):
        return True
    if section_id == "sec-observation":
        return True
    if section_id == "sec-reasoning":
        return bool(thesis_overlap(text, thesis) or len(text) <= DUMP_CHAR_LIMIT)
    return False


def weakens_thesis(text: str, thesis: Mapping[str, Any] | None) -> bool:
    """Drop paragraphs that undo the central consultation."""
    if not thesis:
        return False
    direction = str(thesis.get("corrective_direction") or "").casefold()
    lowered = text.casefold()
    if not direction:
        return False
    if "ngoại lệ" in lowered and direction and direction not in lowered:
        if thesis_overlap(text, thesis):
            return False
        return True
    return False


def thesis_overlap(text: str, thesis: Mapping[str, Any] | None) -> bool:
    """True when paragraph tokens share the case thesis."""
    tokens = thesis_tokens(thesis)
    if not tokens:
        return False
    words = meaning_tokens(text)
    return bool(tokens & words)


def thesis_tokens(thesis: Mapping[str, Any] | None) -> frozenset[str]:
    """Customer-visible thesis tokens used to keep the consultation coherent."""
    if not thesis:
        return frozenset()
    parts = [
        str(thesis.get("title") or ""),
        str(thesis.get("short_thesis") or ""),
        str(thesis.get("core_tension") or ""),
        str(thesis.get("corrective_direction") or ""),
        str(thesis.get("career_implication") or ""),
    ]
    return meaning_tokens(" ".join(parts))


def meaning_tokens(text: str) -> frozenset[str]:
    """Tokens for meaning-level comparison, not exact-string equality."""
    return frozenset(
        token
        for token in _WORD.findall(normalize_text(text).casefold())
        if token not in _STOPWORDS
    )


def sentence_count(text: str) -> int:
    """Count customer sentences in one node. Empty text is zero."""
    blob = normalize_text(text)
    if not blob:
        return 0
    parts = [part for part in _SENTENCE.split(blob) if part.strip()]
    return max(len(parts), 1)


def word_count(text: str) -> int:
    """Count whitespace-separated tokens."""
    return len(normalize_text(text).split()) if normalize_text(text) else 0
