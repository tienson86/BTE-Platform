"""Load Cân Xương lookup tables from CSV. No calculation."""

from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path

from engines.can_xuong_engine.exceptions import CanXuongLookupError

_REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE_PATH = _REPO_ROOT / "database" / "21_can_xuong"


def _norm(value: str) -> str:
    return " ".join(value.strip().split())


class CanXuongLoader:
    """Read-only CSV loader for year / month / day / hour weights and copy."""

    def __init__(self, database_path: str | Path | None = None) -> None:
        self.database_path = Path(database_path) if database_path else DEFAULT_DATABASE_PATH

    def _read(self, filename: str) -> list[dict[str, str]]:
        path = self.database_path / filename
        if not path.is_file():
            raise CanXuongLookupError(f"Missing Cân Xương table: {path}")
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return [{str(k): str(v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]

    @lru_cache(maxsize=1)
    def year_weights(self) -> dict[str, int]:
        """Map Hoa Giáp label → trọng lượng (chỉ)."""
        table: dict[str, int] = {}
        for row in self._read("01_nam.csv"):
            key = _norm(row.get("hoa_giap") or "")
            if key:
                table[key] = int(row["trong_luong_chi"])
        return table

    @lru_cache(maxsize=1)
    def month_weights(self) -> dict[int, int]:
        """Map lunar month 1–12 → trọng lượng (chỉ)."""
        return {int(row["thang_am"]): int(row["trong_luong_chi"]) for row in self._read("02_thang.csv")}

    @lru_cache(maxsize=1)
    def day_weights(self) -> dict[int, int]:
        """Map lunar day 1–30 → trọng lượng (chỉ)."""
        return {int(row["ngay_am"]): int(row["trong_luong_chi"]) for row in self._read("03_ngay.csv")}

    @lru_cache(maxsize=1)
    def hour_weights(self) -> dict[str, int]:
        """Map Địa Chi giờ → trọng lượng (chỉ)."""
        table: dict[str, int] = {}
        for row in self._read("04_gio.csv"):
            key = _norm(row.get("dia_chi") or "")
            if key:
                table[key] = int(row["trong_luong_chi"])
        return table

    def classification_row(self, total_chi: int) -> dict[str, str]:
        """Resolve classification band for a total weight in chỉ."""
        for row in self._read("05_phan_loai.csv"):
            lo = int(row["min_chi"])
            hi = int(row["max_chi"])
            if lo <= total_chi <= hi:
                return row
        raise CanXuongLookupError(f"No classification band for total_chi={total_chi}")

    def interpretation_row(self, total_chi: int) -> dict[str, str]:
        """Resolve interpretation copy for an exact total, else empty."""
        for row in self._read("06_luan_giai.csv"):
            if int(row["tong_chi"]) == total_chi:
                return row
        return {}
