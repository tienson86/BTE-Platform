"""V1.0 Pattern → Useful God override eligibility.

Detection of a special Pattern does not grant Overall Useful God override.
PAT-R1 LEVEL-1 chuyên remain visible. G1-X01 published follow remains eligible.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .conflict import FOLLOW_EXCLUSIVE_PATTERNS, SPECIAL_EXCLUSIVE_PATTERNS
from .follow_tokens import canonicalize_follow_token

# PAT-R1: all production spe_* tokens are LEVEL 1.
LEVEL_1_SPECIAL_TOKENS: frozenset[str] = SPECIAL_EXCLUSIVE_PATTERNS

# Published follow after G1-X01 Strength + detector is LEVEL 2.
LEVEL_2_FOLLOW_TOKENS: frozenset[str] = FOLLOW_EXCLUSIVE_PATTERNS

SPECIAL_SHORT_LABELS: dict[str, str] = {
    "khuc_truc": "Khúc Trực",
    "viem_thuong": "Viêm Thượng",
    "nhuan_ha": "Nhuận Hạ",
    "gia_sac": "Giá Sắc",
    "jia_wang": "Giá Vượng",
}

DETECTED_SPECIAL_PREFIX = "Cấu trúc đặc biệt được nhận diện: "


@dataclass(slots=True)
class PatternOverrideClassification:
    """Authority split: detected Pattern vs Overall Useful God override."""

    qualification_level: int | None
    ug_override_eligible: bool
    detected_special_pattern: str | None
    follow_pattern: str | None


def classify_pattern_override(
    pattern: str | None,
    follow_type: str | None = None,
) -> PatternOverrideClassification:
    """Classify a published Pattern winner for Useful God override authority.

    V1.0:
    - Published follow token (G1-X01 gated): LEVEL 2, eligible.
    - LEVEL-1 chuyên (spe_*): detected, not eligible.
    - Ordinary / combination: no special override.
    """
    follow = canonicalize_follow_token(follow_type)
    token = str(pattern or "").strip().lower() or None
    if follow:
        detected = token if token in LEVEL_1_SPECIAL_TOKENS else None
        return PatternOverrideClassification(
            qualification_level=2,
            ug_override_eligible=True,
            detected_special_pattern=detected,
            follow_pattern=follow,
        )
    if token in LEVEL_1_SPECIAL_TOKENS:
        return PatternOverrideClassification(
            qualification_level=1,
            ug_override_eligible=False,
            detected_special_pattern=token,
            follow_pattern=None,
        )
    if token in LEVEL_2_FOLLOW_TOKENS:
        return PatternOverrideClassification(
            qualification_level=2,
            ug_override_eligible=True,
            detected_special_pattern=None,
            follow_pattern=token,
        )
    return PatternOverrideClassification(
        qualification_level=None,
        ug_override_eligible=False,
        detected_special_pattern=None,
        follow_pattern=None,
    )


def resolve_context_override_eligible(context: Any) -> bool:
    """Whether spc_* may enter Overall competition for this Useful God context.

    Explicit ``ug_override_eligible`` wins. Unset contexts with a canonical
    follow token remain eligible so G1-X01 synthetic tests keep working.
    """
    explicit = getattr(context, "ug_override_eligible", None)
    if explicit is True:
        return True
    if explicit is False:
        return False
    follow = canonicalize_follow_token(getattr(context, "follow_pattern", None))
    return follow is not None


def detected_special_display_label(token: str | None) -> str:
    """Neutral customer wording for an under-qualified detected chuyên."""
    key = str(token or "").strip().lower()
    short = SPECIAL_SHORT_LABELS.get(key)
    if not short:
        return ""
    return f"{DETECTED_SPECIAL_PREFIX}{short}"
