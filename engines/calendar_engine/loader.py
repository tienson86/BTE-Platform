"""
BTE Platform - Calendar Loader.

Chịu trách nhiệm nạp dữ liệu cho Calendar Engine.
Không thực hiện tính toán.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from engines.core.base_loader import BaseLoader


class CalendarLoader(BaseLoader):
    """
    Loader của Calendar Engine.
    """

    def __init__(self, data_dir: str | Path | None = None) -> None:

        super().__init__()

        if data_dir is None:
            data_dir = (
                Path(__file__).resolve().parent / "data"
            )

        self.data_dir = Path(data_dir)

        self._cache: dict[str, Any] = {}

    # =====================================================
    # Generic
    # =====================================================

    def load(self, name: str) -> Any:
        """
        Load dữ liệu theo tên.
        """

        if name in self._cache:
            return self._cache[name]

        method_name = f"load_{name}"

        if not hasattr(self, method_name):
            raise ValueError(
                f"Không tìm thấy loader '{method_name}'."
            )

        data = getattr(self, method_name)()

        self._cache[name] = data

        return data

    def clear_cache(self) -> None:

        self._cache.clear()

    # =====================================================
    # Solar Terms
    # =====================================================

    def load_solar_terms(self):

        return self.load_csv(
            self.data_dir / "solar_terms.csv"
        )

    # =====================================================
    # New Moon
    # =====================================================

    def load_new_moons(self):

        return self.load_csv(
            self.data_dir / "newmoon.csv"
        )

    # =====================================================
    # Delta T
    # =====================================================

    def load_delta_t(self):

        return self.load_csv(
            self.data_dir / "delta_t.csv"
        )

    # =====================================================
    # Periodic Longitude
    # =====================================================

    def load_periodic_longitude(self):

        return self.load_csv(
            self.data_dir /
            "periodic_longitude.csv"
        )

    # =====================================================
    # Periodic Latitude
    # =====================================================

    def load_periodic_latitude(self):

        return self.load_csv(
            self.data_dir /
            "periodic_latitude.csv"
        )

    # =====================================================
    # Periodic Distance
    # =====================================================

    def load_periodic_distance(self):

        return self.load_csv(
            self.data_dir /
            "periodic_distance.csv"
        )

    # =====================================================
    # Leap Month
    # =====================================================

    def load_leap_month_rules(self):

        return self.load_json(
            self.data_dir /
            "leap_month.json"
        )

    # =====================================================
    # Cache
    # =====================================================

    @property
    def cache(self):

        return self._cache
