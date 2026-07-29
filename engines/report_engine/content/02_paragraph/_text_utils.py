"""Polarity + topic helpers shared by the Paragraph Layer."""

from __future__ import annotations

import re
import unicodedata
from typing import Any, Mapping

_TOKEN_RE = re.compile(r"[a-zA-ZÀ-ỹ0-9_]+", re.UNICODE)

_STOP = frozenset(
    {
        "va",
        "cua",
        "cac",
        "mot",
        "la",
        "cho",
        "voi",
        "trong",
        "khi",
        "neu",
        "and",
        "or",
        "the",
        "to",
        "of",
        "a",
        "an",
        "in",
        "on",
        "for",
        "co",
        "khong",
        "duoc",
        "se",
        "thi",
        "nhu",
        "de",
        "tai",
    }
)

_POS = ("positive", "pos", "+", "thuan", "tot", "loi", "manh", "vuong")
_NEG = ("negative", "neg", "-", "bat", "xau", "hai", "yeu", "nhuoc", "warning", "warn")


def fold(text: str) -> str:
    """Remove accents for stable token keys."""
    decomposed = unicodedata.normalize("NFD", text.strip().lower())
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def tokenize(text: str, *, min_len: int = 3) -> list[str]:
    """Tokenize text into topic candidates."""
    tokens: list[str] = []
    for match in _TOKEN_RE.findall(fold(text)):
        token = match.lower()
        if len(token) < min_len or token in _STOP or token.isdigit():
            continue
        tokens.append(token)
    return tokens


def extract_text(rule: Mapping[str, Any]) -> str:
    """Best available sentence text from a grouped rule."""
    for key in ("sentence", "description", "message", "rule_name"):
        value = str(rule.get(key) or "").strip()
        if value:
            return value
    return ""


def detect_polarity(rule: Mapping[str, Any], text: str) -> str:
    """
    Resolve polarity from explicit field, else lexical cues.

    Returns: positive | negative | neutral
    """
    raw = str(rule.get("polarity") or "").strip().lower()
    if raw in {"positive", "pos", "+"}:
        return "positive"
    if raw in {"negative", "neg", "-", "warning", "warn"}:
        return "negative"
    if raw == "neutral":
        return "neutral"

    folded = fold(text)
    has_pos = any(marker in folded for marker in _POS)
    has_neg = any(marker in folded for marker in _NEG)
    if has_pos and not has_neg:
        return "positive"
    if has_neg and not has_pos:
        return "negative"
    return "neutral"


def topic_key(text: str, keywords: list[str] | None = None) -> str:
    """
    Pick a topic key for merging.

    Prefer ContentContext keywords present in text; else first content token.
    """
    tokens = tokenize(text)
    if not tokens:
        return "general"
    if keywords:
        present = [kw for kw in keywords if kw in tokens]
        if present:
            return present[0]
    return tokens[0]


def priority_of(rule: Mapping[str, Any]) -> float:
    """Numeric priority for ranking inside a paragraph."""
    for key in ("priority", "confidence", "score"):
        try:
            return float(rule.get(key) or 0)
        except (TypeError, ValueError):
            continue
    return 0.0
