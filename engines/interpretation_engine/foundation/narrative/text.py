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
