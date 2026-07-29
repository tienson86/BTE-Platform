from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(slots=True)
class SolarTerm:
    """Một tiết khí tại thời điểm truy vấn."""

    name: str
    index: int


@dataclass(slots=True)
class SolarTermMonth:
    """Nguyệt lệnh (tháng Bát Tự) suy từ tiết khí."""

    month_index: int
    branch: str
    branch_index: int
    start_term: str
    start_term_index: int


class SolarTermEngine:
    """
    Xác định tiết khí và nguyệt lệnh từ bảng ngày chuẩn V1.0.

    Tháng Bát Tự đổi theo 12 Tiết (Lập Xuân, Kinh Trập, ... Tiểu Hàn),
    không theo tháng dương lịch.
    """

    _names: tuple[str, ...] = (
        "Lập Xuân",
        "Vũ Thủy",
        "Kinh Trập",
        "Xuân Phân",
        "Thanh Minh",
        "Cốc Vũ",
        "Lập Hạ",
        "Tiểu Mãn",
        "Mang Chủng",
        "Hạ Chí",
        "Tiểu Thử",
        "Đại Thử",
        "Lập Thu",
        "Xử Thử",
        "Bạch Lộ",
        "Thu Phân",
        "Hàn Lộ",
        "Sương Giáng",
        "Lập Đông",
        "Tiểu Tuyết",
        "Đại Tuyết",
        "Đông Chí",
        "Tiểu Hàn",
        "Đại Hàn",
    )

    # 12 Tiết mở đầu nguyệt lệnh (month_index 1..12 → Dần..Sửu)
    _MONTH_START_TERM_INDEX: tuple[int, ...] = (
        0,
        2,
        4,
        6,
        8,
        10,
        12,
        14,
        16,
        18,
        20,
        22,
    )

    _MONTH_BRANCHES: tuple[str, ...] = (
        "Dần",
        "Mão",
        "Thìn",
        "Tỵ",
        "Ngọ",
        "Mùi",
        "Thân",
        "Dậu",
        "Tuất",
        "Hợi",
        "Tý",
        "Sửu",
    )

    def __init__(self) -> None:
        self._base_dates = self._load_base_dates()

    @staticmethod
    @lru_cache(maxsize=1)
    def _load_base_dates() -> tuple[dict[str, str], ...]:
        """Đọc solar_term_base_dates.csv (tháng/ngày xấp xỉ V1.0)."""
        path = Path(__file__).resolve().parent / "data" / "solar_term_base_dates.csv"
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = tuple(dict(row) for row in csv.DictReader(handle))
        if len(rows) != 24:
            raise ValueError(f"solar_term_base_dates.csv phải có 24 dòng, nhận {len(rows)}")
        return rows

    def list_terms(self, year: int) -> list[SolarTerm]:
        """Danh sách 24 tiết khí của một năm dương lịch."""
        del year
        return [SolarTerm(name=name, index=index) for index, name in enumerate(self._names)]

    def get_term_datetime_parts(self, year: int, term_index: int) -> tuple[int, int, int]:
        """Trả về (year, month, day) của tiết khí theo bảng chuẩn."""
        row = self._base_dates[term_index % 24]
        return year, int(row["month"]), int(row["day"])

    def get_li_chun(self, year: int) -> tuple[int, int, int]:
        """Ngày Lập Xuân của năm dương lịch ``year``."""
        return self.get_term_datetime_parts(year, 0)

    def _term_sort_key(self, year: int, term_index: int) -> tuple[int, int, int]:
        y, m, d = self.get_term_datetime_parts(year, term_index)
        return (y, m, d)

    def get_current_term(self, year: int, month: int, day: int) -> SolarTerm:
        """
        Tiết khí hiện hành tại ngày dương lịch.

        Lấy tiết khí gần nhất có ngày bắt đầu <= ngày truy vấn,
        xét cả các tiết cuối năm trước (phạm vi Đông chí → Lập Xuân).
        """
        target = (year, month, day)
        candidates: list[tuple[tuple[int, int, int], int]] = []
        for term_year in (year - 1, year):
            for term_index in range(24):
                key = self._term_sort_key(term_year, term_index)
                if key <= target:
                    candidates.append((key, term_index))
        if not candidates:
            # Trước mọi tiết của year-1 — dùng Đại Hàn năm trước nữa.
            return SolarTerm(name=self._names[23], index=23)
        _key, term_index = max(candidates, key=lambda item: item[0])
        return SolarTerm(name=self._names[term_index], index=term_index)

    def get_bazi_month(self, year: int, month: int, day: int) -> SolarTermMonth:
        """
        Nguyệt lệnh Bát Tự tại ngày dương lịch.

        Tháng Dần bắt đầu từ Lập Xuân; tháng Sửu bắt đầu từ Tiểu Hàn.
        """
        target = (year, month, day)
        best: tuple[tuple[int, int, int], int] | None = None
        for term_year in (year - 1, year):
            for month_index, term_index in enumerate(self._MONTH_START_TERM_INDEX, start=1):
                key = self._term_sort_key(term_year, term_index)
                if key <= target and (best is None or key > best[0]):
                    best = (key, month_index)
        if best is None:
            month_index = 12
        else:
            month_index = best[1]
        branch = self._MONTH_BRANCHES[month_index - 1]
        start_term_index = self._MONTH_START_TERM_INDEX[month_index - 1]
        branch_order = (
            "Tý",
            "Sửu",
            "Dần",
            "Mão",
            "Thìn",
            "Tỵ",
            "Ngọ",
            "Mùi",
            "Thân",
            "Dậu",
            "Tuất",
            "Hợi",
        )
        return SolarTermMonth(
            month_index=month_index,
            branch=branch,
            branch_index=branch_order.index(branch),
            start_term=self._names[start_term_index],
            start_term_index=start_term_index,
        )

    def is_after_li_chun(self, year: int, month: int, day: int) -> bool:
        """True nếu (year, month, day) đã tới hoặc qua Lập Xuân của năm đó."""
        _y, li_month, li_day = self.get_li_chun(year)
        return (month, day) >= (li_month, li_day)

    get_term = get_current_term
