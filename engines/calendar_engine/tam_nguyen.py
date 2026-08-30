"""Tam Nguyên Cửu Vận — 180-year Flying Star cycle.

Calendar Engine owns the cycle. Ganzhi Cung lookups must use the Nguyên of
the civil year; they must not assume Hạ Nguyên.
"""

from __future__ import annotations

from dataclasses import dataclass

from engines.calendar_engine.exceptions import CalendarValidationError

CYCLE_YEARS = 180
YUAN_YEARS = 60
PERIOD_YEARS = 20
PERIOD_COUNT = 9

# Giáp Tý opening Thượng Nguyên vận 1 of the current 180-year cycle.
TAM_NGUYEN_EPOCH_YEAR = 1864

THUONG_NGUYEN = "Thượng Nguyên"
TRUNG_NGUYEN = "Trung Nguyên"
HA_NGUYEN = "Hạ Nguyên"

YUAN_ORDER: tuple[str, str, str] = (THUONG_NGUYEN, TRUNG_NGUYEN, HA_NGUYEN)

_YUAN_BY_PERIOD: dict[int, str] = {
    1: THUONG_NGUYEN,
    2: THUONG_NGUYEN,
    3: THUONG_NGUYEN,
    4: TRUNG_NGUYEN,
    5: TRUNG_NGUYEN,
    6: TRUNG_NGUYEN,
    7: HA_NGUYEN,
    8: HA_NGUYEN,
    9: HA_NGUYEN,
}


@dataclass(slots=True)
class TamNguyenResult:
    """Civil-year placement in the 180-year Tam Nguyên Cửu Vận cycle."""

    tam_nguyen: str
    cuu_van: int
    cycle_start_year: int
    yuan_start_year: int
    period_start_year: int
    period_end_year: int

    def to_dict(self) -> dict[str, str | int]:
        """Serialize cycle fields for CalendarResult / API."""
        return {
            "tam_nguyen": self.tam_nguyen,
            "cuu_van": self.cuu_van,
            "cycle_start_year": self.cycle_start_year,
            "yuan_start_year": self.yuan_start_year,
            "period_start_year": self.period_start_year,
            "period_end_year": self.period_end_year,
        }


def _cycle_offset(year: int) -> int:
    if int(year) < 1:
        raise CalendarValidationError(f"invalid civil year for Tam Nguyên: {year}")
    return int(year) - TAM_NGUYEN_EPOCH_YEAR


def cycle_start_year(year: int) -> int:
    """Return the Giáp Tý year that opens the 180-year cycle containing ``year``."""
    offset = _cycle_offset(year)
    cycles_behind = offset // CYCLE_YEARS
    return TAM_NGUYEN_EPOCH_YEAR + cycles_behind * CYCLE_YEARS


def cuu_van_for_year(year: int) -> int:
    """Return Cửu Vận period 1–9 for a Gregorian year."""
    position = _cycle_offset(year) % CYCLE_YEARS
    return position // PERIOD_YEARS + 1


def tam_nguyen_for_year(year: int) -> str:
    """Return Thượng / Trung / Hạ Nguyên for a Gregorian year."""
    return _YUAN_BY_PERIOD[cuu_van_for_year(year)]


def yuan_start_year(year: int, tam_nguyen: str | None = None) -> int:
    """Giáp Tý year that opens the 60-year Nguyên containing ``year``."""
    label = tam_nguyen or tam_nguyen_for_year(year)
    try:
        yuan_index = YUAN_ORDER.index(label)
    except ValueError as exc:
        raise CalendarValidationError(f"unknown Tam Nguyên: {tam_nguyen!r}") from exc
    return cycle_start_year(year) + yuan_index * YUAN_YEARS


def calculate_tam_nguyen(year: int) -> TamNguyenResult:
    """Place a Gregorian year in Tam Nguyên Cửu Vận."""
    van = cuu_van_for_year(year)
    cycle_start = cycle_start_year(year)
    position = _cycle_offset(year) % CYCLE_YEARS
    period_index = van - 1
    period_start = cycle_start + period_index * PERIOD_YEARS
    return TamNguyenResult(
        tam_nguyen=_YUAN_BY_PERIOD[van],
        cuu_van=van,
        cycle_start_year=cycle_start,
        yuan_start_year=cycle_start + (period_index // 3) * YUAN_YEARS,
        period_start_year=period_start,
        period_end_year=period_start + PERIOD_YEARS - 1,
    )
