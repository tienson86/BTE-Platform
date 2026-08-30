"""Build FourPillarIdentity from already-computed Can Chi labels.

Reuses Date Selection ``pillar_contract``. Year/Month Cung follow Calendar
Tam Nguyên when provided; Day/Hour stay on Hạ Nguyên.
Does not recompute Calendar or Bazi. Does not load a second lookup table.
"""

from __future__ import annotations

from typing import Any

from engines.date_selection.identity import pillar_contract
from engines.identity.models import FourPillarIdentity, PillarIdentity

_PILLAR_KEYS = ("year", "month", "day", "hour")
_PILLAR_TYPES = {
    "year": "Year",
    "month": "Month",
    "day": "Day",
    "hour": "Hour",
}


def _ganzhi_label(pillar: Any) -> str:
    """``Stem Branch`` from a chart pillar or BaziView pillar."""
    stem = getattr(pillar, "stem", None)
    branch = getattr(pillar, "branch", None)
    if stem and branch:
        return f"{stem} {branch}".strip()
    raise ValueError("pillar must expose stem and branch")


def _split_can_chi(can_chi: str) -> tuple[str, str]:
    """Split an existing Can Chi label. Does not compute stems."""
    parts = can_chi.split()
    if len(parts) >= 2:
        return parts[0], parts[1]
    return can_chi, ""


def pillar_identity_from_ganzhi(
    ganzhi: str,
    pillar_type: str = "Day",
    *,
    tam_nguyen: str | None = None,
    reference_year: int | None = None,
) -> PillarIdentity:
    """Resolve one pillar identity from a Hoa Giáp label.

    Day/Hour omit ``tam_nguyen`` and keep the Hạ Nguyên Cung row.
    Year/Month pass Calendar Tam Nguyên.
    """
    if tam_nguyen and reference_year is not None:
        cell = pillar_contract(
            ganzhi,
            tam_nguyen=tam_nguyen,
            reference_year=reference_year,
        )
    else:
        cell = pillar_contract(ganzhi)
    can_chi = cell["can_chi"]
    stem, branch = _split_can_chi(can_chi)
    return PillarIdentity(
        stem=stem,
        branch=branch,
        can_chi=can_chi,
        nayin_element=cell["nayin_element"],
        cung_phi=cell["cung_phi"],
        pillar_type=pillar_type,
    )


def four_pillar_identity_from_labels(
    year: str,
    month: str,
    day: str,
    hour: str,
    *,
    tam_nguyen: str | None = None,
    reference_year: int | None = None,
) -> FourPillarIdentity:
    """Build four-pillar identity from four Can Chi labels."""
    return FourPillarIdentity(
        year=pillar_identity_from_ganzhi(
            year,
            _PILLAR_TYPES["year"],
            tam_nguyen=tam_nguyen,
            reference_year=reference_year,
        ),
        month=pillar_identity_from_ganzhi(
            month,
            _PILLAR_TYPES["month"],
            tam_nguyen=tam_nguyen,
            reference_year=reference_year,
        ),
        day=pillar_identity_from_ganzhi(day, _PILLAR_TYPES["day"]),
        hour=pillar_identity_from_ganzhi(hour, _PILLAR_TYPES["hour"]),
    )


def four_pillar_identity_from_bazi(
    bazi: Any,
    *,
    tam_nguyen: str | None = None,
    reference_year: int | None = None,
) -> FourPillarIdentity:
    """Build four-pillar identity from a BaziView or BaziChart."""
    return four_pillar_identity_from_labels(
        _ganzhi_label(bazi.year_pillar),
        _ganzhi_label(bazi.month_pillar),
        _ganzhi_label(bazi.day_pillar),
        _ganzhi_label(bazi.hour_pillar),
        tam_nguyen=tam_nguyen,
        reference_year=reference_year,
    )


def four_pillar_keys() -> tuple[str, ...]:
    """Stable Year → Hour key order."""
    return _PILLAR_KEYS
