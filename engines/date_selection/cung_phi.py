"""Resolve Cung Phi from 60 Hoa Giáp + canonical gender."""

from __future__ import annotations

from engines.date_selection.constants import (
    FEMALE_GENDER_ALIASES,
    GENDER_LABELS,
    MALE_GENDER_ALIASES,
    YANG_STEMS,
)
from engines.date_selection.exceptions import DateSelectionValidationError
from engines.date_selection.loader import load_hoa_giap_cung_phi
from engines.date_selection.models import TrachInfo
from engines.date_selection.trach import trach_from_cung


def normalize_gender(gender: str | None) -> str:
    """
    Return canonical ``male`` / ``female``.

    Never defaults a missing or invalid gender.
    """
    if gender is None or str(gender).strip() == "":
        raise DateSelectionValidationError("gender is required")
    key = str(gender).strip().lower()
    if key in MALE_GENDER_ALIASES:
        return "male"
    if key in FEMALE_GENDER_ALIASES:
        return "female"
    raise DateSelectionValidationError(f"unsupported gender: {gender!r}")


def gender_label(gender: str) -> str:
    """Customer-facing Nam / Nữ."""
    return GENDER_LABELS[normalize_gender(gender)]


def _normalize_ganzhi(ganzhi: str) -> str:
    text = " ".join((ganzhi or "").split())
    if not text:
        raise DateSelectionValidationError("ganzhi is required")
    return text


def _row_for_ganzhi(ganzhi: str) -> dict[str, str]:
    table = load_hoa_giap_cung_phi()
    key = _normalize_ganzhi(ganzhi)
    row = table.get(key)
    if row is None:
        collapsed = key.replace(" ", "")
        for candidate, value in table.items():
            if candidate.replace(" ", "") == collapsed:
                return value
        raise DateSelectionValidationError(f"unknown Ganzhi: {ganzhi!r}")
    return row


def cung_for_ganzhi(ganzhi: str, gender: str) -> str:
    """Return Cung Nam or Cung Nữ for a 60 Hoa Giáp label."""
    row = _row_for_ganzhi(ganzhi)
    sex = normalize_gender(gender)
    cung = row["cung_nam"] if sex == "male" else row["cung_nu"]
    if not cung:
        raise DateSelectionValidationError(f"missing Cung Phi for {ganzhi!r}")
    return cung


def trach_for_ganzhi(ganzhi: str, gender: str) -> TrachInfo:
    """Resolve Cung Phi, element, and trạch group from Ganzhi + gender."""
    return trach_from_cung(cung_for_ganzhi(ganzhi, gender))


def polarity_gender_from_ganzhi(ganzhi: str) -> str:
    """
    Infer a lookup gender from stem polarity for unpersonalized screens.

    Dương stem → male column, Âm stem → female column.
    """
    key = _normalize_ganzhi(ganzhi)
    stem = key.split(" ", 1)[0]
    if stem in YANG_STEMS:
        return "male"
    return "female"


def trach_for_ganzhi_unpersonalized(ganzhi: str) -> TrachInfo:
    """Day/hour Cung Phi when the caller has no personal gender."""
    return trach_for_ganzhi(ganzhi, polarity_gender_from_ganzhi(ganzhi))
