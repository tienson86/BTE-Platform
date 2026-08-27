"""Date Selection hour/khắc civil-clock convention.

Calendar/Bazi ``hour_branch.csv`` keeps ``07:00–08:59`` semantics.
This adapter is Date Selection V1.0 display and slot arithmetic only.

Odd ``HH:00`` belongs to the previous two-hour branch (inclusive close).
Example: ``07:00`` is Mão; ``07:01`` starts Thìn; ``09:00`` closes Thìn.
"""

from __future__ import annotations

from engines.date_selection.constants import BRANCH_INDEX, BRANCHES, DS_HOUR_WINDOWS
from engines.date_selection.exceptions import DateSelectionError
from engines.date_selection.models import HourWindow


def date_selection_hour_windows() -> tuple[HourWindow, ...]:
    """Return the twelve Date Selection conventional hour windows."""
    windows: list[HourWindow] = []
    for branch, start_hour, start_minute, end_hour, end_minute, cross in DS_HOUR_WINDOWS:
        windows.append(
            HourWindow(
                branch=branch,
                branch_index=BRANCH_INDEX[branch],
                start_hour=start_hour,
                start_minute=start_minute,
                end_hour=end_hour,
                end_minute=end_minute,
                time_range=(
                    f"{start_hour:02d}:{start_minute:02d}–{end_hour:02d}:{end_minute:02d}"
                ),
                is_cross_day=cross,
            )
        )
    if len(windows) != len(BRANCHES):
        raise DateSelectionError("Date Selection hour convention must contain 12 windows")
    return tuple(windows)


def window_containing_clock(
    windows: tuple[HourWindow, ...],
    hour: int,
    minute: int,
) -> HourWindow:
    """Resolve the Date Selection hour that contains local clock time."""
    minutes = hour * 60 + minute
    for window in windows:
        start = window.start_hour * 60 + window.start_minute
        end = window.end_hour * 60 + window.end_minute
        if window.is_cross_day:
            if minutes >= start or minutes <= end:
                return window
            continue
        if start <= minutes <= end:
            return window
    raise DateSelectionError(f"no Date Selection hour window for {hour:02d}:{minute:02d}")
