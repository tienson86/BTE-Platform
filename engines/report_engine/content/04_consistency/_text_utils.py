"""Normalize text for consistency comparisons."""

from __future__ import annotations

import re
import unicodedata


def normalize(text: str) -> str:
    """Fold accents and whitespace."""
    decomposed = unicodedata.normalize("NFD", str(text or "").strip().lower())
    plain = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", plain).strip()


_ANTONYM_PAIRS: tuple[tuple[str, str], ...] = (
    ("manh", "yeu"),
    ("vuong", "nhuoc"),
    ("tot", "xau"),
    ("thuan", "nghich"),
    ("loi", "hai"),
    ("thuan loi", "bat loi"),
    ("positive", "negative"),
)


def has_antonym_clash(left: str, right: str) -> bool:
    """True when each side carries opposite lexical poles."""
    a_text = normalize(left)
    b_text = normalize(right)
    if not a_text or not b_text:
        return False
    for pos, neg in _ANTONYM_PAIRS:
        left_pos, left_neg = pos in a_text, neg in a_text
        right_pos, right_neg = pos in b_text, neg in b_text
        if (left_pos and left_neg) or (right_pos and right_neg):
            continue
        if (left_pos and right_neg) or (left_neg and right_pos):
            return True
    return False


def polarity_conflict(left: str, right: str) -> bool:
    """True for positive vs negative/warning polarity pair."""
    a = (left or "neutral").lower()
    b = (right or "neutral").lower()
    pos = {"positive", "pos", "+"}
    neg = {"negative", "neg", "-", "warning", "warn"}
    return (a in pos and b in neg) or (a in neg and b in pos)
