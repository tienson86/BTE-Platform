"""Liushi (Lưu thì) runtime data provider."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from ..models import LiushiPeriod
from ._common import (
    day_ganzhi,
    day_master_of,
    enrich_stem,
    hour_pillar_for,
    resolve_reference_dt,
)


class DefaultLiushiProvider:
    """Hourly runtime model via calendar conversion only."""

    def __init__(self, *, reference_dt: datetime | None = None) -> None:
        """Optional reference datetime (defaults to now)."""
        self.reference_dt = reference_dt

    def provide(
        self,
        *,
        calendar: Any,
        bazi: Any,
        liuri: Any | None = None,
    ) -> LiushiPeriod:
        """Return hour pillar for the reference civil datetime."""
        reference = resolve_reference_dt(calendar, self.reference_dt)
        day_master = day_master_of(bazi)

        if liuri is not None and getattr(liuri, "heavenly_stem", None):
            day_stem = str(liuri.heavenly_stem)
            year = int(liuri.year)
            month = int(liuri.month)
            day = int(liuri.day)
        else:
            year, month, day = reference.year, reference.month, reference.day
            day_stem, _ = day_ganzhi(year, month, day)

        stem, branch = hour_pillar_for(day_stem, reference.hour)
        fields = enrich_stem(stem, branch, day_master)
        return LiushiPeriod(
            year=year,
            month=month,
            day=day,
            hour=reference.hour,
            minute=reference.minute,
            ganzhi=fields["ganzhi"],
            heavenly_stem=fields["heavenly_stem"],
            earthly_branch=fields["earthly_branch"],
            element=fields["element"],
            yin_yang=fields["yin_yang"],
            ten_god=fields["ten_god"],
            hidden_stems=fields["hidden_stems"],
            metadata={
                "kind": "liushi",
                "source": "ngu_thu_don",
                "day_stem": day_stem,
                "sprint": "4.1",
            },
        )
