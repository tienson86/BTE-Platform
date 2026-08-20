"""Canonical gender for Analyze / Luck: internal male/female, display Nam/Nữ."""

from __future__ import annotations

from engines.luck_engine.exceptions import LuckContextError
from engines.luck_engine.providers._common import (
    GENDER_LABELS,
    gender_display_label,
    normalize_luck_gender,
)

from applications.api.exceptions import ValidationAPIError

__all__ = [
    "GENDER_LABELS",
    "gender_display_label",
    "normalize_luck_gender",
    "require_canonical_gender",
]


def require_canonical_gender(gender: str | None) -> str:
    """
    Return canonical ``male`` / ``female`` or raise ValidationAPIError.

    Analyze must not default missing gender to male.
    """
    try:
        return normalize_luck_gender(gender)
    except LuckContextError as exc:
        message = str(exc)
        if message == "gender_required":
            raise ValidationAPIError(
                "gender is required",
                details={"field": "gender", "code": "gender_required"},
            ) from exc
        raise ValidationAPIError(
            "invalid gender",
            details={"field": "gender", "code": "unsupported_gender"},
        ) from exc
