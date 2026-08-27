"""BTE Date Selection Engine V1.0 — auspicious date lookup and ranking."""

from __future__ import annotations

from engines.date_selection.cung_phi import trach_for_ganzhi
from engines.date_selection.exceptions import DateSelectionError, DateSelectionValidationError
from engines.date_selection.models import (
    CalendarSnapshot,
    DaySelection,
    MonthCalendar,
    PersonProfile,
    SearchResult,
    SixStateResult,
    TrachInfo,
)
from engines.date_selection.service import DateSelectionEngine, DateSelectionService
from engines.date_selection.trach import cung_to_element, cung_to_trach_group

__all__ = [
    "CalendarSnapshot",
    "DateSelectionEngine",
    "DateSelectionError",
    "DateSelectionService",
    "DateSelectionValidationError",
    "DaySelection",
    "MonthCalendar",
    "PersonProfile",
    "SearchResult",
    "SixStateResult",
    "TrachInfo",
    "cung_to_element",
    "cung_to_trach_group",
    "trach_for_ganzhi",
]
