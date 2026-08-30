"""Sum Cân Xương lookup weights. No BaZi / Tam Nguyên logic."""

from __future__ import annotations

from engines.can_xuong_engine.exceptions import CanXuongLookupError
from engines.can_xuong_engine.loader import CanXuongLoader, _norm
from engines.can_xuong_engine.models import CAN_XUONG_RULE_VERSION, CAN_XUONG_SOURCE, CanXuongResult


def format_display_weight(total_chi: int) -> tuple[int, int, str]:
    """Split chỉ into lượng / chỉ and a display string."""
    liang, chi = divmod(int(total_chi), 10)
    return liang, chi, f"{liang} lượng {chi} chỉ"


class CanXuongCalculator:
    """Look up four traditional weights and add them."""

    def __init__(self, loader: CanXuongLoader | None = None) -> None:
        self.loader = loader or CanXuongLoader()

    def calculate(
        self,
        *,
        year_ganzhi: str,
        lunar_month: int,
        lunar_day: int,
        hour_branch: str,
    ) -> CanXuongResult:
        """Resolve Cân Xương from year Hoa Giáp, lunar month/day, and hour branch."""
        year_key = _norm(year_ganzhi)
        hour_key = _norm(hour_branch)
        year_chi = self.loader.year_weights().get(year_key)
        if year_chi is None:
            raise CanXuongLookupError(f"Unknown year Hoa Giáp: {year_ganzhi!r}")
        month_chi = self.loader.month_weights().get(int(lunar_month))
        if month_chi is None:
            raise CanXuongLookupError(f"Unknown lunar month: {lunar_month!r}")
        day_chi = self.loader.day_weights().get(int(lunar_day))
        if day_chi is None:
            raise CanXuongLookupError(f"Unknown lunar day: {lunar_day!r}")
        hour_chi = self.loader.hour_weights().get(hour_key)
        if hour_chi is None:
            raise CanXuongLookupError(f"Unknown hour branch: {hour_branch!r}")
        total = year_chi + month_chi + day_chi + hour_chi
        liang, chi, display = format_display_weight(total)
        band = self.loader.classification_row(total)
        copy = self.loader.interpretation_row(total)
        summary = copy.get("tom_tat") or band.get("tom_tat") or ""
        interpretation = copy.get("luan_giai") or summary
        return CanXuongResult(
            total_weight=total,
            liang=liang,
            chi=chi,
            display_weight=display,
            classification=band.get("phan_loai") or "",
            rating=band.get("danh_gia") or "",
            summary=summary,
            interpretation=interpretation,
            source=CAN_XUONG_SOURCE,
            version=CAN_XUONG_RULE_VERSION,
            year_chi=year_chi,
            month_chi=month_chi,
            day_chi=day_chi,
            hour_chi=hour_chi,
            year_ganzhi=year_key,
            lunar_month=int(lunar_month),
            lunar_day=int(lunar_day),
            hour_branch=hour_key,
        )
