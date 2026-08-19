"""Canonical Ten Gods mapping — wraps ``engines.bazi_engine.ten_god``."""

from __future__ import annotations

from engines.bazi_engine.ten_god import (
    day_master_element,
    day_master_yin_yang,
    ten_god_name,
)

from engines.ten_gods_engine.constants import (
    DAY_MASTER_LABEL,
    GOD_ID_TO_LABEL,
    LABEL_TO_GOD_ID,
)
from engines.ten_gods_engine.exceptions import TenGodsValidationError


def map_stem_to_ten_god(
    day_master: str,
    stem: str,
    *,
    pillar: str | None = None,
    visibility: str = "visible",
) -> tuple[str, str]:
    """Map a heavenly stem to Vietnamese label and canonical god_id.

    Ten God relationship always comes from ``ten_god_name`` (same stem → Tỷ Kiên).
    Nhật Chủ is a presentation role for the day pillar heavenly stem only.
    """
    if _is_day_heavenly_stem(
        day_master=day_master,
        stem=stem,
        pillar=pillar,
        visibility=visibility,
    ):
        return DAY_MASTER_LABEL, "day_master"

    label = ten_god_name(day_master, stem)
    if not label:
        raise TenGodsValidationError(
            f"Unable to map stem '{stem}' for day master '{day_master}'",
        )

    god_id = LABEL_TO_GOD_ID.get(label)
    if god_id is None:
        raise TenGodsValidationError(
            f"Unknown Ten God label '{label}' for stem '{stem}'",
        )
    return label, god_id


def _is_day_heavenly_stem(
    *,
    day_master: str,
    stem: str,
    pillar: str | None,
    visibility: str,
) -> bool:
    """True only for the visible Day Pillar heavenly stem."""
    return (
        stem == day_master
        and pillar == "day"
        and visibility == "visible"
    )


def day_master_info(stem: str) -> dict[str, str]:
    """Return published day master element and yin-yang."""
    element = day_master_element(stem)
    yin_yang = day_master_yin_yang(stem)
    if not element or not yin_yang:
        raise TenGodsValidationError(f"Unknown day master stem '{stem}'")
    return {
        "stem": stem,
        "element": element,
        "yin_yang": yin_yang,
    }


def label_for_god_id(god_id: str) -> str:
    """Resolve display label for a god_id."""
    if god_id == "day_master":
        return DAY_MASTER_LABEL
    label = GOD_ID_TO_LABEL.get(god_id)
    if label is None:
        raise TenGodsValidationError(f"Unknown god_id '{god_id}'")
    return label
