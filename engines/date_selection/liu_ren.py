"""Six-state remainder mapping used by day, hour, and khắc."""

from __future__ import annotations

from engines.date_selection.constants import SIX_STATE_BY_REMAINDER
from engines.date_selection.exceptions import DateSelectionValidationError
from engines.date_selection.models import SixStateResult


def six_state_from_value(value: int) -> SixStateResult:
    """
    Map an integer value onto the six public classifications.

    Remainder 0 is Không Vong. Do not rewrite a 0 remainder as 6.
    """
    remainder = int(value) % 6
    try:
        code, label = SIX_STATE_BY_REMAINDER[remainder]
    except KeyError as exc:
        raise DateSelectionValidationError(f"invalid remainder: {remainder}") from exc
    return SixStateResult(remainder=remainder, code=code, label=label)


def day_value(year_branch_index: int, lunar_month: int, lunar_day: int) -> int:
    """DAY_VALUE = lunar year branch index + lunar month + lunar day."""
    return int(year_branch_index) + int(lunar_month) + int(lunar_day)


def hour_value(day_total: int, hour_branch_index: int) -> int:
    """HOUR_VALUE = DAY_VALUE + hour branch index."""
    return int(day_total) + int(hour_branch_index)


def ke_value(hour_total: int, ke_index: int) -> int:
    """KE_VALUE = HOUR_VALUE + khắc index (1..6)."""
    return int(hour_total) + int(ke_index)
