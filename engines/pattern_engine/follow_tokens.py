"""Canonical follow-pattern tokens shared by Pattern and Useful God.

Machine token travels between engines. Display labels stay presentation-only.
"""

from __future__ import annotations

from typing import Any

# Canonical tokens (SSOT). Useful God special rules match these, not labels.
FOLLOW_DISPLAY_BY_TOKEN: dict[str, str] = {
    "tong_tai": "Tòng Tài",
    "tong_quan": "Tòng Quan",
    "tong_sat": "Tòng Sát",
    "tong_nhi": "Tòng Nhi",
    "tong_an": "Tòng Ấn",
    "tong_vuong": "Tòng Vượng",
}

# Weak-follow / cực-nhược family. Incompatible with canonical Strength `strong`.
WEAK_FOLLOW_TOKENS: frozenset[str] = frozenset(
    {
        "tong_tai",
        "tong_quan",
        "tong_sat",
        "tong_nhi",
        "tong_an",
    }
)

# Tòng Vượng / chuyên vượng. Not gated by the cực-nhược rule.
STRONG_FOLLOW_TOKENS: frozenset[str] = frozenset({"tong_vuong"})

_CANONICAL_STRENGTH: frozenset[str] = frozenset({"strong", "weak", "balanced"})

_DISPLAY_TO_TOKEN: dict[str, str] = {
    label: token for token, label in FOLLOW_DISPLAY_BY_TOKEN.items()
}
_DISPLAY_TO_TOKEN.update(
    {
        "Tòng Cường": "tong_vuong",
        "Tòng Thế": "tong_vuong",
    }
)


def canonicalize_follow_token(value: str | None) -> str | None:
    """Map a display label or token to the canonical follow token."""
    text = str(value or "").strip()
    if not text:
        return None
    if text in FOLLOW_DISPLAY_BY_TOKEN:
        return text
    mapped = _DISPLAY_TO_TOKEN.get(text)
    if mapped:
        return mapped
    lowered = text.lower().replace(" ", "_")
    if lowered in FOLLOW_DISPLAY_BY_TOKEN:
        return lowered
    return None


def follow_display_label(value: str | None) -> str:
    """Vietnamese display label for a follow token or legacy label."""
    token = canonicalize_follow_token(value)
    if token is None:
        return ""
    return FOLLOW_DISPLAY_BY_TOKEN[token]


def canonical_strength_level(context_or_level: Any) -> str | None:
    """Read canonical Strength class from PatternContext, StrengthResult, or str."""
    if context_or_level is None:
        return None
    if isinstance(context_or_level, str):
        text = context_or_level.strip().lower()
        return text if text in _CANONICAL_STRENGTH else None

    level = getattr(context_or_level, "strength_level", None)
    if not level:
        strength = getattr(context_or_level, "strength", None)
        if strength is None:
            strength = getattr(context_or_level, "strength_result", None)
        if isinstance(strength, dict):
            level = strength.get("strength_level") or strength.get("level")
        elif strength is not None:
            level = getattr(strength, "strength_level", None) or getattr(
                strength, "level", None
            )
    if not level and isinstance(context_or_level, dict):
        level = context_or_level.get("strength_level") or context_or_level.get("level")
    text = str(level or "").strip().lower()
    return text if text in _CANONICAL_STRENGTH else None


def follow_token_eligible(token: str | None, strength_level: str | None) -> bool:
    """Whether a follow token may publish for the given canonical Strength class.

    V1.0:
    - weak-follow (Tòng Tài/Quan/Sát/Nhi/Ấn): only ``weak``.
    - Tòng Vượng: only ``strong`` (not the cực-nhược gate).
    - ``balanced``: never automatic follow.
    """
    canonical = canonicalize_follow_token(token)
    level = canonical_strength_level(strength_level)
    if canonical is None or level is None:
        return False
    if canonical in WEAK_FOLLOW_TOKENS:
        return level == "weak"
    if canonical in STRONG_FOLLOW_TOKENS:
        return level == "strong"
    return False
