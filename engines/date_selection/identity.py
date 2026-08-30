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


def pillar_contract(
    ganzhi: str,
    *,
    tam_nguyen: str | None = None,
    reference_year: int | None = None,
) -> dict[str, str]:
    """
    Canonical Four Pillars cell for one Hoa Giáp label.

    Day/Hour (no ``tam_nguyen``) keep the Hạ Nguyên Cung CSV.
    Year/Month pass Calendar Tam Nguyên and resolve Cung from that dataset.
    Does not return the full Nạp âm name.
    """
    from engines.calendar_engine.cung_phi import cung_for_ganzhi
    from engines.date_selection.cung_phi import trach_for_date_ganzhi
    from engines.date_selection.trach import trach_from_cung

    if tam_nguyen:
        year = int(reference_year) if reference_year is not None else 1984
        cung = cung_for_ganzhi(
            ganzhi,
            tam_nguyen=tam_nguyen,
            reference_year=year,
            gender="male",
        )
        trach = trach_from_cung(cung)
    else:
        trach = trach_for_date_ganzhi(ganzhi)
    view = hoa_giap_view(ganzhi, trach)
    cung_name = view["cung"]
    if not cung_name:
        raise DateSelectionValidationError(f"missing Cung Phi for {ganzhi!r}")
    return {
        "can_chi": view["ganzhi"],
        "nayin_element": view["nayin_element"],
        "cung_phi": cung_name,
    }


def routed_pillar_contract(
    ganzhi: str,
    *,
    tam_nguyen: str,
    reference_year: int,
) -> dict[str, str]:
    """``pillar_contract`` plus the Nguyên that supplied the Cung row."""
    cell = pillar_contract(
        ganzhi,
        tam_nguyen=tam_nguyen,
        reference_year=reference_year,
    )
    return {**cell, "source_nguyen": tam_nguyen}


def snapshot_pillar_payloads(calendar: Any) -> dict[str, dict[str, str]]:
    """Year/Month use the snapshot Tam Nguyên; Day stays Hạ Nguyên."""
    from engines.calendar_engine.tam_nguyen import HA_NGUYEN, tam_nguyen_for_year

    year = int(calendar.solar_year)
    yuan = (calendar.tam_nguyen or "").strip() or tam_nguyen_for_year(year)
    return {
        "year": routed_pillar_contract(
            calendar.year_ganzhi,
            tam_nguyen=yuan,
            reference_year=year,
        ),
        "month": routed_pillar_contract(
            calendar.month_ganzhi,
            tam_nguyen=yuan,
            reference_year=year,
        ),
        "day": routed_pillar_contract(
            calendar.day_ganzhi,
            tam_nguyen=HA_NGUYEN,
            reference_year=year,
        ),
    }
