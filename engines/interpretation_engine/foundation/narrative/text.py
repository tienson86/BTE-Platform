"""Text helpers for composition — normalize and fingerprint, never invent."""

from __future__ import annotations

import re

from engines.interpretation_engine.foundation.narrative.constants import (
    MIN_CUSTOMER_PROSE_CHARS,
)

_WHITESPACE = re.compile(r"\s+")
_ENGINE_PAIR = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\s*[=:]")
_GRAPH_EDGE = re.compile(r".+->.+->.+")
_NUMERIC_ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=-?\d")
_BARE_ENGINE_TOKENS = frozenset(
    {"year", "month", "day", "hour", "strong", "weak", "normal"}
)
_BROKEN_FRAGMENT = re.compile(
    r"\(\s*\)|Tách vs\s*\.|trong\s*,|khi nói\s+\.|:\s*$"
)
_DISCLAIMER_PHRASES = (
    "Không hứa hiệu quả tài chính.",
    "Không chẩn đoán, không báo bệnh.",
    "Không chẩn đoán.",
)
_IMPLEMENTATION_TERMS = (
    "decision explanation",
    "strength engine",
    "production phải",
    "cả hai key",
    "cùng hit",
    "group priority",
    "candidate group",
    "assessment",
    r"\bstems\b",
)


def normalize_text(value: str) -> str:
    """Collapse whitespace so copied statements compare stably."""
    return _WHITESPACE.sub(" ", str(value or "").strip())


def fingerprint(value: str) -> str:
    """Identity of an idea for deduplication. Not a new claim."""
    return normalize_text(value).casefold()


def is_customer_prose(value: str) -> bool:
    """True when copied text is readable by a customer, not an engine dump."""
    text = normalize_text(value)
    if len(text) < MIN_CUSTOMER_PROSE_CHARS:
        return False
    if text.casefold() in _BARE_ENGINE_TOKENS:
        return False
    if is_broken_fragment(text):
        return False
    if _ENGINE_PAIR.match(text) or _GRAPH_EDGE.match(text.replace(" ", "")):
        return False
    if _NUMERIC_ASSIGNMENT.search(text):
        return False
    if "group priority" in text.casefold():
        return False
    if "=" in text:
        left = text.split("=", 1)[0].strip()
        if " " not in left and len(left) <= 12:
            return False
    return True


def is_broken_fragment(value: str) -> bool:
    """True when copied text still contains empty or truncated fragments."""
    text = normalize_text(value)
    if not text:
        return False
    if "()" in text or "( )" in text:
        return True
    return bool(_BROKEN_FRAGMENT.search(text))


def collapse_repeated_disclaimer(value: str) -> str:
    """Keep at most one copy of a repeated ethical disclaimer."""
    text = normalize_text(value)
    for phrase in _DISCLAIMER_PHRASES:
        if text.count(phrase) > 1:
            first = text.find(phrase)
            text = text[: first + len(phrase)] + text[first + len(phrase) :].replace(
                phrase, ""
            )
            text = normalize_text(text)
    return text


def implementation_language_hits(value: str) -> tuple[str, ...]:
    """Return implementation-term hits that must not reach the customer."""
    text = normalize_text(value)
    if not text:
        return ()
    lowered = text.casefold()
    hits: list[str] = []
    for term in _IMPLEMENTATION_TERMS:
        if term.startswith("\\") or term.startswith("r\\") or "\\b" in term:
            if re.search(term, text, flags=re.IGNORECASE):
                hits.append(term)
            continue
        if term in lowered:
            hits.append(term)
    return tuple(hits)
