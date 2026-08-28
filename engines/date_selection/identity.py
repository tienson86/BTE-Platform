"""Nạp âm (Mệnh) versus Cung Phi identity for a Hoa Giáp label."""

from __future__ import annotations

from typing import Any

from engines.date_selection.exceptions import DateSelectionValidationError
from engines.date_selection.loader import load_nap_am
from engines.date_selection.models import TrachInfo


def _normalize_ganzhi(ganzhi: str) -> str:
    text = " ".join((ganzhi or "").split())
    if not text:
        raise DateSelectionValidationError("ganzhi is required")
    return text


def nayin_for_ganzhi(ganzhi: str) -> tuple[str, str]:
    """
    Return ``(nap_am_name, menh_element)`` for a 60 Hoa Giáp label.

    ``menh_element`` is the workbook Mệnh field (e.g. Mậu Thìn → Mộc).
    It is not the Cung Phi element.
    """
    key = _normalize_ganzhi(ganzhi)
    table = load_nap_am()
    row = table.get(key)
    if row is None:
        collapsed = key.replace(" ", "")
        for candidate, value in table.items():
            if candidate.replace(" ", "") == collapsed:
                row = value
                break
    if row is None:
        raise DateSelectionValidationError(f"unknown Ganzhi: {ganzhi!r}")
    return row[0], row[1]


def hoa_giap_view(ganzhi: str, trach: TrachInfo | None) -> dict[str, Any]:
    """Explicit Date Selection identity fields for API / UI."""
    _, menh = nayin_for_ganzhi(ganzhi)
    return {
        "ganzhi": _normalize_ganzhi(ganzhi),
        "nayin": menh,
        "nayin_element": menh,
        "cung": trach.cung if trach else None,
        "cung_element": trach.element_label if trach else None,
        "trach_group": trach.trach_group_code if trach else None,
        "trach_group_label": trach.trach_group_label if trach else None,
    }


def pillar_contract(ganzhi: str) -> dict[str, str]:
    """
    Canonical Four Pillars cell for one Hoa Giáp label.

    Uses the same Hạ Nguyên Cung and Nạp âm element lookup already applied
    to Day and Hour. Does not return the full Nạp âm name.
    """
    from engines.date_selection.cung_phi import trach_for_date_ganzhi

    view = hoa_giap_view(ganzhi, trach_for_date_ganzhi(ganzhi))
    cung = view["cung"]
    if not cung:
        raise DateSelectionValidationError(f"missing Cung Phi for {ganzhi!r}")
    return {
        "can_chi": view["ganzhi"],
        "nayin_element": view["nayin_element"],
        "cung_phi": cung,
    }
