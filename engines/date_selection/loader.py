"""Load canonical calendar / Cung Phi datasets for Date Selection."""

from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path

from engines.date_selection.constants import (
    BRANCHES,
    CUNG_ELEMENT,
    HA_NGUYEN_CUNG_CSV,
    HOA_GIAP_CUNG_PHI_CSV,
    HOUR_GANZHI_CSV,
    JIAZI_LABELS,
    NAP_AM_CSV,
)
from engines.date_selection.exceptions import DateSelectionError
from engines.date_selection.hour_convention import (
    date_selection_hour_windows,
    window_containing_clock,
)
from engines.date_selection.models import HourWindow

REPO_ROOT = Path(__file__).resolve().parents[2]


def _read_csv(relative: str) -> list[dict[str, str]]:
    path = REPO_ROOT / relative
    if not path.is_file():
        raise DateSelectionError(f"missing dataset: {relative}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


@lru_cache(maxsize=1)
def load_hour_windows() -> tuple[HourWindow, ...]:
    """Load Date Selection conventional hour windows (not Bazi hour_branch.csv)."""
    windows = date_selection_hour_windows()
    if len(windows) != len(BRANCHES):
        raise DateSelectionError("Date Selection hour convention must contain 12 windows")
    return windows


@lru_cache(maxsize=1)
def load_hour_ganzhi_map() -> dict[tuple[str, str], str]:
    """Load day-stem group × hour branch → hour stem from calendar data."""
    mapping: dict[tuple[str, str], str] = {}
    for row in _read_csv(HOUR_GANZHI_CSV):
        group = row["nhom_can_ngay"].strip()
        branch = row["chi_gio"].strip()
        stem = row["can_gio"].strip()
        mapping[(group, branch)] = stem
    return mapping


@lru_cache(maxsize=1)
def load_nap_am() -> dict[str, tuple[str, str]]:
    """Load Nạp Âm name + ngũ hành keyed by Hoa Giáp label."""
    table: dict[str, tuple[str, str]] = {}
    for row in _read_csv(NAP_AM_CSV):
        key = " ".join(row["hoa_giap"].split())
        table[key] = (row["nap_am"].strip(), row["ngu_hanh"].strip())
    return table


@lru_cache(maxsize=1)
def load_ha_nguyen_cung() -> dict[str, dict[str, str]]:
    """Load the 60-row intrinsic Hạ Nguyên date/hour Cung table."""
    from engines.date_selection.trach import trach_from_cung

    table: dict[str, dict[str, str]] = {}
    for row in _read_csv(HA_NGUYEN_CUNG_CSV):
        key = " ".join(row["ganzhi"].split())
        cung = (row.get("ha_nguyen_cung") or "").strip()
        if key in table:
            raise DateSelectionError(f"duplicate Hạ Nguyên Ganzhi: {key!r}")
        if cung not in CUNG_ELEMENT:
            raise DateSelectionError(f"invalid Hạ Nguyên Cung for {key!r}: {cung!r}")
        info = trach_from_cung(cung)
        element = (row.get("cung_element") or "").strip()
        group = (row.get("trach_group") or "").strip()
        if element != info.element_label:
            raise DateSelectionError(
                f"Hạ Nguyên element mismatch for {key!r}: {element!r}"
            )
        if group != info.trach_group_code:
            raise DateSelectionError(
                f"Hạ Nguyên trạch mismatch for {key!r}: {group!r}"
            )
        table[key] = {
            "ha_nguyen_cung": cung,
            "cung_element": info.element_label,
            "trach_group": info.trach_group_code,
        }
    expected = set(JIAZI_LABELS)
    if set(table) != expected:
        missing = sorted(expected - set(table))
        extra = sorted(set(table) - expected)
        raise DateSelectionError(
            f"Hạ Nguyên table must contain the 60 Hoa Giáp; missing={missing} extra={extra}"
        )
    return table


@lru_cache(maxsize=1)
def load_hoa_giap_cung_phi() -> dict[str, dict[str, str]]:
    """Load 60 Hoa Giáp person Cung Nam/Nữ helper table."""
    table: dict[str, dict[str, str]] = {}
    for row in _read_csv(HOA_GIAP_CUNG_PHI_CSV):
        key = " ".join(row["ganzhi"].split())
        table[key] = {
            "nap_am": row["nap_am"].strip(),
            "ngu_hanh": row["ngu_hanh"].strip(),
            "cung_nam": row["cung_nam"].strip(),
            "cung_nu": row["cung_nu"].strip(),
            "cung_ngay": (row.get("cung_ngay") or "").strip(),
            "reference_year": row["reference_year"].strip(),
        }
    if len(table) != 60:
        raise DateSelectionError("hoa_giap_cung_phi.csv must contain 60 rows")
    return table


def hour_window_for_branch(branch: str) -> HourWindow:
    """Return the canonical window for a traditional hour branch."""
    for window in load_hour_windows():
        if window.branch == branch:
            return window
    raise DateSelectionError(f"unknown hour branch: {branch!r}")


def hour_window_for_clock(hour: int, minute: int) -> HourWindow:
    """Resolve the Date Selection hour that contains local clock time."""
    return window_containing_clock(load_hour_windows(), hour, minute)
