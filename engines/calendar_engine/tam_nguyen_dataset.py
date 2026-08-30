"""Tam Nguyên 60 Hoa Giáp dataset — Year/Month Can Chi source of truth.

Year and Month heavenly stem / earthly branch are looked up from
``tam_nguyen_60_hoa_giap.csv``. They are not computed by GanzhiAlgorithm.year.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from engines.calendar_engine.exceptions import CalendarValidationError
from engines.calendar_engine.month_ganzhi import (
    bazi_year_number,
    month_stem_for,
    solar_term_month,
)
from engines.calendar_engine.solar_terms.engine import SolarTermEngine
from engines.calendar_engine.tam_nguyen import (
    HA_NGUYEN,
    tam_nguyen_for_year,
    yuan_start_year,
)

CALENDAR_RULE_VERSION = "G1-10C"
DATASET_NAME = "tam_nguyen_60_hoa_giap.csv"

_DATA_PATH = Path(__file__).resolve().parent / "data" / DATASET_NAME


@dataclass(slots=True)
class DatasetJiaziRow:
    """One 60 Hoa Giáp row inside a Tam Nguyên block."""

    tam_nguyen: str
    index: int
    heavenly_stem: str
    earthly_branch: str
    ganzhi: str
    nap_am: str
    sample_year: int

    def to_dict(self) -> dict[str, str | int]:
        """Serialize one dataset row."""
        return {
            "tam_nguyen": self.tam_nguyen,
            "index": self.index,
            "heavenly_stem": self.heavenly_stem,
            "earthly_branch": self.earthly_branch,
            "ganzhi": self.ganzhi,
            "nap_am": self.nap_am,
            "sample_year": self.sample_year,
        }


@dataclass(slots=True)
class ResolvedGanzhiPillar:
    """Complete Year or Month pillar taken from the Tam Nguyên dataset."""

    heavenly_stem: str
    earthly_branch: str
    ganzhi: str
    nap_am: str
    source_nguyen: str

    def to_dict(self) -> dict[str, str]:
        """Serialize resolved Can Chi plus Nguyên."""
        return {
            "heavenly_stem": self.heavenly_stem,
            "earthly_branch": self.earthly_branch,
            "ganzhi": self.ganzhi,
            "nap_am": self.nap_am,
            "source_nguyen": self.source_nguyen,
        }


@lru_cache(maxsize=1)
def load_tam_nguyen_hoa_giap() -> dict[tuple[str, int], DatasetJiaziRow]:
    """Load the three 60-row Tam Nguyên Hoa Giáp tables. Loader only."""
    if not _DATA_PATH.is_file():
        raise CalendarValidationError(f"missing Tam Nguyên dataset: {_DATA_PATH}")
    table: dict[tuple[str, int], DatasetJiaziRow] = {}
    with _DATA_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        for raw in csv.DictReader(handle):
            yuan = (raw.get("tam_nguyen") or "").strip()
            index = int(raw["thu_tu"])
            stem = (raw.get("thien_can") or "").strip()
            branch = (raw.get("dia_chi") or "").strip()
            row = DatasetJiaziRow(
                tam_nguyen=yuan,
                index=index,
                heavenly_stem=stem,
                earthly_branch=branch,
                ganzhi=(raw.get("hoa_giap") or f"{stem} {branch}").strip(),
                nap_am=(raw.get("nap_am") or "").strip(),
                sample_year=int(raw["nam_mau"]),
            )
            table[(yuan, index)] = row
    if len(table) != 180:
        raise CalendarValidationError(
            f"{DATASET_NAME} must contain 180 rows, got {len(table)}"
        )
    return table


def _dataset_year(
    year: int,
    month: int | None = None,
    day: int | None = None,
) -> int:
    """Civil year used to index the Tam Nguyên 60 Hoa Giáp table.

    When month/day are present, the index year changes at Lập Xuân so January
    dates still read the previous Nguyên-table row. Stem/branch still come
    from that row, never from GanzhiAlgorithm.year.
    """
    if month is None or day is None:
        return int(year)
    return bazi_year_number(int(year), int(month), int(day), SolarTermEngine())


def jiazi_row_for_year(
    year: int,
    tam_nguyen: str | None = None,
    *,
    month: int | None = None,
    day: int | None = None,
) -> DatasetJiaziRow:
    """Return the 60 Hoa Giáp row for a Gregorian date in its Nguyên table."""
    lookup_year = _dataset_year(year, month, day)
    yuan = tam_nguyen or tam_nguyen_for_year(lookup_year)
    start = yuan_start_year(lookup_year, yuan)
    index = (int(lookup_year) - start) % 60
    try:
        return load_tam_nguyen_hoa_giap()[(yuan, index)]
    except KeyError as exc:
        raise CalendarValidationError(
            f"no Hoa Giáp row for year={lookup_year} tam_nguyen={yuan!r} index={index}"
        ) from exc


def jiazi_row_at(tam_nguyen: str, index: int) -> DatasetJiaziRow:
    """Return the dataset row at ``index`` (0–59) of one Nguyên table."""
    try:
        return load_tam_nguyen_hoa_giap()[(tam_nguyen, int(index))]
    except KeyError as exc:
        raise CalendarValidationError(
            f"no Hoa Giáp row for tam_nguyen={tam_nguyen!r} index={index}"
        ) from exc


def nap_am_for_ganzhi(ganzhi: str) -> str:
    """Nạp âm of a 60 Hoa Giáp label from the Tam Nguyên dataset."""
    text = " ".join((ganzhi or "").split())
    for row in load_tam_nguyen_hoa_giap().values():
        if row.ganzhi == text:
            return row.nap_am
    raise CalendarValidationError(f"unknown Ganzhi in Tam Nguyên dataset: {ganzhi!r}")


def resolve_year_pillar(
    calendar_year: int,
    tam_nguyen: str | None = None,
    *,
    month: int | None = None,
    day: int | None = None,
) -> ResolvedGanzhiPillar:
    """Year Can Chi from the Tam Nguyên 60 Hoa Giáp table."""
    row = jiazi_row_for_year(calendar_year, tam_nguyen, month=month, day=day)
    return ResolvedGanzhiPillar(
        heavenly_stem=row.heavenly_stem,
        earthly_branch=row.earthly_branch,
        ganzhi=row.ganzhi,
        nap_am=row.nap_am,
        source_nguyen=row.tam_nguyen,
    )


def resolve_month_pillar(
    year: int,
    month: int,
    day: int,
    tam_nguyen: str | None = None,
) -> ResolvedGanzhiPillar:
    """Month Can Chi using the Year stem from the Tam Nguyên dataset.

    Month branch is nguyệt lệnh (12 Tiết). Month stem is Ngũ Hổ Độn from
    the dataset Year stem — not GanzhiAlgorithm.year.
    """
    year_pillar = resolve_year_pillar(year, tam_nguyen, month=month, day=day)
    info = solar_term_month(year, month, day)
    stem = month_stem_for(year_pillar.heavenly_stem, info.month_index)
    ganzhi = f"{stem} {info.branch}"
    yuan = year_pillar.source_nguyen
    return ResolvedGanzhiPillar(
        heavenly_stem=stem,
        earthly_branch=info.branch,
        ganzhi=ganzhi,
        nap_am=nap_am_for_ganzhi(ganzhi),
        source_nguyen=yuan,
    )


def resolve_day_source_nguyen() -> str:
    """Day Can Chi stays on Hạ Nguyên."""
    return HA_NGUYEN


def resolve_hour_source_nguyen() -> str:
    """Hour Can Chi stays on Hạ Nguyên."""
    return HA_NGUYEN
