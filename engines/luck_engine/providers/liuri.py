"""Liuri (Lưu nhật) runtime data provider."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from ..models import LiuriPeriod
from ._common import day_ganzhi, day_master_of, enrich_stem, resolve_reference_dt


class DefaultLiuriProvider:
    """Daily runtime model via calendar conversion only."""

    def __init__(self, *, reference_dt: datetime | None = None) -> None:
        """Optional reference date (defaults to now)."""
        self.reference_dt = reference_dt

    def provide(
        self,
        *,
        calendar: Any,
        bazi: Any,
        liuyue: Any | None = None,
    ) -> LiuriPeriod:
        """Return day pillar for the reference civil date."""
        del liuyue
        reference = resolve_reference_dt(calendar, self.reference_dt)
        day_master = day_master_of(bazi)
        stem, branch = day_ganzhi(reference.year, reference.month, reference.day)
        fields = enrich_stem(stem, branch, day_master)
        return LiuriPeriod(
            year=reference.year,
            month=reference.month,
            day=reference.day,
            ganzhi=fields["ganzhi"],
            heavenly_stem=fields["heavenly_stem"],
            earthly_branch=fields["earthly_branch"],
            element=fields["element"],
            yin_yang=fields["yin_yang"],
            ten_god=fields["ten_god"],
            hidden_stems=fields["hidden_stems"],
            metadata={
                "kind": "liuri",
                "source": "julian_day_ganzhi",
                "sprint": "4.1",
            },
        )
