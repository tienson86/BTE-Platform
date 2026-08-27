"""Load canonical calendar / Cung Phi datasets for Date Selection."""

from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path

from engines.date_selection.constants import (
    BRANCH_INDEX,
    BRANCHES,
    HOA_GIAP_CUNG_PHI_CSV,
    HOUR_BRANCH_CSV,
    HOUR_GANZHI_CSV,
    NAP_AM_CSV,
)
from engines.date_selection.exceptions import DateSelectionError
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
    """Load canonical traditional hour windows from hour_branch.csv."""
    windows: list[HourWindow] = []
    for row in _read_csv(HOUR_BRANCH_CSV):
        branch = row["branch"].strip()
        start_hour = int(row["start_hour"])
        start_minute = int(row["start_minute"])
        end_hour = int(row["end_hour"])
        end_minute = int(row["end_minute"])
        windows.append(
            HourWindow(
                branch=branch,
                branch_index=BRANCH_INDEX[branch],
                start_hour=start_hour,
                start_minute=start_minute,
                end_hour=end_hour,
                end_minute=end_minute,
                time_range=f"{start_hour:02d}:{start_minute:02d}–{end_hour:02d}:{end_minute:02d}",
                is_cross_day=row.get("is_cross_day", "0").strip() == "1",
            )
        )
    if len(windows) != len(BRANCHES):
        raise DateSelectionError("hour_branch.csv must contain 12 windows")
    return tuple(windows)


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
def load_hoa_giap_cung_phi() -> dict[str, dict[str, str]]:
    """Load 60 Hoa Giáp Cung Nam / Cung Nữ derived from canonical Feng Shui."""
    table: dict[str, dict[str, str]] = {}
    for row in _read_csv(HOA_GIAP_CUNG_PHI_CSV):
        key = " ".join(row["ganzhi"].split())
        table[key] = {
            "nap_am": row["nap_am"].strip(),
            "ngu_hanh": row["ngu_hanh"].strip(),
            "cung_nam": row["cung_nam"].strip(),
            "cung_nu": row["cung_nu"].strip(),
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
    """Resolve the traditional hour that contains local clock time."""
    minutes = hour * 60 + minute
    for window in load_hour_windows():
        start = window.start_hour * 60 + window.start_minute
        end = window.end_hour * 60 + window.end_minute
        if window.is_cross_day:
            if minutes >= start or minutes <= end:
                return window
            continue
        if start <= minutes <= end:
            return window
    raise DateSelectionError(f"no hour window for {hour:02d}:{minute:02d}")
