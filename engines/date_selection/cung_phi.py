"""Resolve Cung Phi for a person vs a date/hour Ganzhi."""

from __future__ import annotations

from engines.date_selection.constants import (
    FEMALE_GENDER_ALIASES,
    GENDER_LABELS,
    MALE_GENDER_ALIASES,
)
from engines.date_selection.exceptions import (
    DateSelectionMappingError,
    DateSelectionValidationError,
)
from engines.date_selection.loader import load_hoa_giap_cung_phi
from engines.date_selection.models import TrachInfo
from engines.date_selection.trach import trach_from_cung
from engines.feng_shui_engine import FengShuiEngine, FengShuiEngineError, FengShuiValidationError


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
    """
    Return Cung Nam or Cung Nữ for a person's 60 Hoa Giáp label.

    This is a person lookup. It must not be used to pick a date/hour Cung.
    """
    row = _row_for_ganzhi(ganzhi)
    sex = normalize_gender(gender)
    cung = row["cung_nam"] if sex == "male" else row["cung_nu"]
    if not cung:
        raise DateSelectionValidationError(f"missing Cung Phi for {ganzhi!r}")
    return cung


def trach_for_ganzhi(ganzhi: str, gender: str) -> TrachInfo:
    """Resolve a PERSON'S Cung Phi, element, and trạch from Ganzhi + gender."""
    return trach_from_cung(cung_for_ganzhi(ganzhi, gender))


def trach_for_person(*, lunar_year: int, gender: str) -> TrachInfo:
    """
    Personal Cung Phi from canonical birth year + gender.

    Uses Feng Shui Engine (year-digit method), not the date/hour table.
    """
    sex = normalize_gender(gender)
    try:
        result = FengShuiEngine().calculate(year=int(lunar_year), gender=sex)
    except (FengShuiEngineError, FengShuiValidationError) as exc:
        raise DateSelectionValidationError(str(exc)) from exc
    return trach_from_cung(result.gua_name)


def cung_for_date_ganzhi(ganzhi: str) -> str:
    """
    Intrinsic Date Selection Cung for a day or hour Ganzhi.

    Gender and stem polarity must not select this value. Requires a canonical
    Hạ Nguyên ``cung_ngay`` mapping; does not invent one from Cung Nam/Nữ.
    """
    row = _row_for_ganzhi(ganzhi)
    cung = (row.get("cung_ngay") or "").strip()
    if not cung:
        raise DateSelectionMappingError(
            "canonical Hạ Nguyên date/hour Cung mapping is missing"
        )
    return cung


def trach_for_date_ganzhi(ganzhi: str) -> TrachInfo:
    """Resolve date/hour Cung Phi from the Hạ Nguyên mapping only."""
    return trach_from_cung(cung_for_date_ganzhi(ganzhi))
