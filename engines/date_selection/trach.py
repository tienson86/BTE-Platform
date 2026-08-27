"""Bagua ngũ hành and Đông/Tây Tứ Trạch resolvers."""

from __future__ import annotations

from engines.date_selection.constants import (
    CUNG_ELEMENT,
    DONG_TU_TRACH,
    TAY_TU_TRACH,
    TRACH_DONG,
    TRACH_TAY,
)
from engines.date_selection.exceptions import DateSelectionValidationError
from engines.date_selection.models import TrachInfo


def cung_to_element(cung: str) -> tuple[str, str]:
    """
    Return ``(element_code, element_label)`` for a Cung Phi name.

    Machine-readable codes: thuy, hoa, moc, kim, tho.
    """
    key = (cung or "").strip()
    try:
        return CUNG_ELEMENT[key]
    except KeyError as exc:
        raise DateSelectionValidationError(f"unknown cung: {cung!r}") from exc


def cung_to_trach_group(cung: str) -> tuple[str, str]:
    """
    Return ``(trach_group_code, trach_group_label)`` for a Cung Phi name.

    Codes: dong, tay. Labels: Đông Tứ Trạch / Tây Tứ Trạch.
    """
    key = (cung or "").strip()
    if key in DONG_TU_TRACH:
        return TRACH_DONG
    if key in TAY_TU_TRACH:
        return TRACH_TAY
    raise DateSelectionValidationError(f"unknown cung: {cung!r}")


def trach_from_cung(cung: str) -> TrachInfo:
    """Build TrachInfo from a Cung Phi display name."""
    element_code, element_label = cung_to_element(cung)
    trach_code, trach_label = cung_to_trach_group(cung)
    return TrachInfo(
        cung=cung.strip(),
        element_code=element_code,
        element_label=element_label,
        trach_group_code=trach_code,
        trach_group_label=trach_label,
    )
