"""Twenty-minute khắc slots inside a canonical traditional hour."""

from __future__ import annotations

from engines.date_selection.constants import KE_COUNT, KE_MINUTES
from engines.date_selection.exceptions import DateSelectionValidationError
from engines.date_selection.liu_ren import ke_value, six_state_from_value
from engines.date_selection.models import HourWindow, KeSlot


def _add_minutes(hour: int, minute: int, delta: int) -> tuple[int, int]:
    total = (hour * 60 + minute + delta) % (24 * 60)
    return divmod(total, 60)


def _format_range(start_h: int, start_m: int, end_h: int, end_m: int) -> str:
    return f"{start_h:02d}:{start_m:02d}–{end_h:02d}:{end_m:02d}"


def ke_slots_for_hour(window: HourWindow, hour_total: int) -> list[KeSlot]:
    """
    Split a Date Selection two-hour window into six 20-minute khắc.

    Start is inclusive; each slot is 20 minutes inclusive. For Thìn
    (07:01–09:00) khắc 1 is 07:01–07:20 and khắc 6 is 08:41–09:00.
    """
    slots: list[KeSlot] = []
    for ke_index in range(1, KE_COUNT + 1):
        offset = (ke_index - 1) * KE_MINUTES
        start_h, start_m = _add_minutes(window.start_hour, window.start_minute, offset)
        end_h, end_m = _add_minutes(
            window.start_hour,
            window.start_minute,
            offset + KE_MINUTES - 1,
        )
        start_minute_of_day = (start_h * 60 + start_m) % (24 * 60)
        slots.append(
            KeSlot(
                ke_index=ke_index,
                time_range=_format_range(start_h, start_m, end_h, end_m),
                start_minute_of_day=start_minute_of_day,
                six_state=six_state_from_value(ke_value(hour_total, ke_index)),
            )
        )
    if len(slots) != KE_COUNT:
        raise DateSelectionValidationError("expected six khắc slots")
    return slots


def current_ke_index(window: HourWindow, hour: int, minute: int) -> int:
    """Return khắc 1..6 for a civil time inside ``window``."""
    clock = hour * 60 + minute
    start = window.start_hour * 60 + window.start_minute
    if window.is_cross_day and clock < start:
        elapsed = (24 * 60 - start) + clock
    else:
        elapsed = clock - start
    index = elapsed // KE_MINUTES + 1
    if index < 1:
        return 1
    if index > KE_COUNT:
        return KE_COUNT
    return int(index)
