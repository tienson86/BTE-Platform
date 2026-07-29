"""Liuyue (Lưu nguyệt) runtime data provider."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from engines.calendar_engine.solar_terms.engine import SolarTermEngine

from ..models import LiuyuePeriod
from ._common import (
    bazi_year_of,
    day_master_of,
    enrich_stem,
    month_stem_for,
    resolve_reference_dt,
    year_ganzhi,
)


class DefaultLiuyueProvider:
    """Generate monthly runtime Liuyue objects (no evaluation)."""

    def __init__(
        self,
        *,
        reference_dt: datetime | None = None,
        terms: SolarTermEngine | None = None,
    ) -> None:
        """Optional reference time for current month selection."""
        self.reference_dt = reference_dt
        self._terms = terms or SolarTermEngine()

    def provide(
        self,
        *,
        calendar: Any,
        bazi: Any,
        liunian: Any | None = None,
    ) -> LiuyuePeriod:
        """Return current-month LiuyuePeriod; year sequence in metadata."""
        reference = resolve_reference_dt(calendar, self.reference_dt)
        day_master = day_master_of(bazi)

        if liunian is not None and getattr(liunian, "year", None):
            year_stem = str(liunian.heavenly_stem)
            bazi_year = int(liunian.year)
        else:
            bazi_year = bazi_year_of(
                reference.year,
                reference.month,
                reference.day,
                self._terms,
            )
            year_stem, _ = year_ganzhi(bazi_year)

        month_info = self._terms.get_bazi_month(
            reference.year,
            reference.month,
            reference.day,
        )
        stem = month_stem_for(year_stem, month_info.month_index)
        branch = month_info.branch
        fields = enrich_stem(stem, branch, day_master)

        year_months: list[dict[str, Any]] = []
        for month_index in range(1, 13):
            m_stem = month_stem_for(year_stem, month_index)
            m_branch = self._terms._MONTH_BRANCHES[month_index - 1]
            start_term = self._terms._names[
                self._terms._MONTH_START_TERM_INDEX[month_index - 1]
            ]
            m_fields = enrich_stem(m_stem, m_branch, day_master)
            year_months.append(
                {
                    "month_index": month_index,
                    "solar_term": start_term,
                    **{
                        k: (list(v) if k == "hidden_stems" else v)
                        for k, v in m_fields.items()
                    },
                }
            )

        return LiuyuePeriod(
            year=bazi_year,
            month=reference.month,
            month_index=month_info.month_index,
            ganzhi=fields["ganzhi"],
            heavenly_stem=fields["heavenly_stem"],
            earthly_branch=fields["earthly_branch"],
            solar_term=month_info.start_term,
            element=fields["element"],
            yin_yang=fields["yin_yang"],
            ten_god=fields["ten_god"],
            hidden_stems=fields["hidden_stems"],
            metadata={
                "kind": "liuyue",
                "civil_year": reference.year,
                "civil_month": reference.month,
                "year_months": year_months,
                "sprint": "4.1",
            },
        )
