"""Liunian (Lưu niên) runtime data provider."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from engines.calendar_engine.solar_terms.engine import SolarTermEngine

from ..models import LiunianPeriod
from ._common import (
    bazi_year_of,
    day_master_of,
    enrich_stem,
    resolve_reference_dt,
    year_ganzhi,
)


class DefaultLiunianProvider:
    """Generate annual runtime Liunian objects (no evaluation)."""

    def __init__(
        self,
        *,
        reference_dt: datetime | None = None,
        terms: SolarTermEngine | None = None,
        span_years: int = 5,
    ) -> None:
        """Optional reference time; nearby years stored in metadata."""
        self.reference_dt = reference_dt
        self._terms = terms or SolarTermEngine()
        self.span_years = span_years

    def provide(
        self,
        *,
        calendar: Any,
        bazi: Any,
        dayun: Any | None = None,
    ) -> LiunianPeriod:
        """Return current-year LiunianPeriod."""
        del dayun
        reference = resolve_reference_dt(calendar, self.reference_dt)
        day_master = day_master_of(bazi)
        bazi_year = bazi_year_of(
            reference.year,
            reference.month,
            reference.day,
            self._terms,
        )
        stem, branch = year_ganzhi(bazi_year)
        fields = enrich_stem(stem, branch, day_master)

        nearby: list[dict[str, Any]] = []
        for offset in range(-self.span_years, self.span_years + 1):
            year = bazi_year + offset
            y_stem, y_branch = year_ganzhi(year)
            y_fields = enrich_stem(y_stem, y_branch, day_master)
            nearby.append(
                {
                    "year": year,
                    **{k: (list(v) if k == "hidden_stems" else v) for k, v in y_fields.items()},
                }
            )

        return LiunianPeriod(
            year=bazi_year,
            ganzhi=fields["ganzhi"],
            heavenly_stem=fields["heavenly_stem"],
            earthly_branch=fields["earthly_branch"],
            element=fields["element"],
            yin_yang=fields["yin_yang"],
            ten_god=fields["ten_god"],
            hidden_stems=fields["hidden_stems"],
            metadata={
                "kind": "liunian",
                "civil_year": reference.year,
                "bazi_year": bazi_year,
                "nearby_years": nearby,
                "sprint": "4.1",
            },
        )
