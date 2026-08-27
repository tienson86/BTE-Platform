"""Hour Ganzhi and traditional hour window helpers."""

from __future__ import annotations

from engines.date_selection.constants import HOUR_STEM_GROUPS
from engines.date_selection.exceptions import DateSelectionError, DateSelectionValidationError
from engines.date_selection.loader import (
    hour_window_for_branch,
    hour_window_for_clock,
    load_hour_ganzhi_map,
    load_hour_windows,
)
from engines.date_selection.models import HourWindow


def hour_ganzhi(day_stem: str, branch: str) -> str:
    """Resolve hour Can Chi from canonical Ngũ Hổ Độn hour table."""
    group = HOUR_STEM_GROUPS.get((day_stem or "").strip())
    if not group:
        raise DateSelectionValidationError(f"unknown day stem: {day_stem!r}")
    stem = load_hour_ganzhi_map().get((group, branch))
    if not stem:
        raise DateSelectionValidationError(
            f"hour Ganzhi not found for {day_stem} / {branch}"
        )
    return f"{stem} {branch}"


def all_hour_windows() -> tuple[HourWindow, ...]:
    """Return the 12 Date Selection conventional hour windows."""
    return load_hour_windows()


def window_for_branch(branch: str) -> HourWindow:
    """Look up a traditional hour by branch name."""
    try:
        return hour_window_for_branch(branch)
    except DateSelectionError as exc:
        raise DateSelectionValidationError(str(exc)) from exc


def window_for_clock(hour: int, minute: int) -> HourWindow:
    """Look up the Date Selection hour containing a civil clock time."""
    return hour_window_for_clock(hour, minute)
