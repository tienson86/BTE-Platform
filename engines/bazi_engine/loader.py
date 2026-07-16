"""
BTE Platform
Bazi Engine Loader

Đọc toàn bộ dữ liệu phục vụ Bazi Engine.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from engines.core.base_loader import BaseLoader


class BaziLoader(BaseLoader):
    """
    Loader của Bazi Engine.
    """

    def __init__(
        self,
        data_dir: str | Path | None = None,
    ) -> None:

        super().__init__()

        if data_dir is None:
            data_dir = (
                Path(__file__).resolve().parent
                / "data"
            )

        self.data_dir = Path(data_dir)

        self._cache: dict[str, Any] = {}

    # =====================================================
    # Generic
    # =====================================================

    def load(self, name: str):

        if name in self._cache:
            return self._cache[name]

        method = getattr(
            self,
            f"load_{name}",
            None,
        )

        if method is None:
            raise ValueError(
                f"Không tồn tại loader '{name}'."
            )

        data = method()

        self._cache[name] = data

        return data

    def clear_cache(self):

        self._cache.clear()

    # =====================================================
    # Load All
    # =====================================================

    def load_all(self):

        self.load_hidden_stems()
        self.load_ten_gods()
        self.load_strength_rules()
        self.load_useful_god_rules()
        self.load_patterns()
        self.load_shensha()
        self.load_combinations()

    # =====================================================
    # Hidden Stems
    # =====================================================

    def load_hidden_stems(self):

        return self.load_csv(
            self.data_dir
            / "hidden_stems.csv"
        )

    # =====================================================
    # Ten Gods
    # =====================================================

    def load_ten_gods(self):

        return self.load_csv(
            self.data_dir
            / "ten_gods.csv"
        )

    # =====================================================
    # Strength
    # =====================================================

    def load_strength_rules(self):

        return self.load_csv(
            self.data_dir
            / "strength_rules.csv"
        )

    # =====================================================
    # Useful God
    # =====================================================

    def load_useful_god_rules(self):

        return self.load_csv(
            self.data_dir
            / "useful_god_rules.csv"
        )

    # =====================================================
    # Pattern
    # =====================================================

    def load_patterns(self):

        return self.load_csv(
            self.data_dir
            / "patterns.csv"
        )

    # =====================================================
    # Shen Sha
    # =====================================================

    def load_shensha(self):

        return self.load_csv(
            self.data_dir
            / "shensha.csv"
        )

    # =====================================================
    # Combination
    # =====================================================

    def load_combinations(self):

        return self.load_csv(
            self.data_dir
            / "combinations.csv"
        )

    # =====================================================
    # Cache
    # =====================================================

    @property
    def cache(self):

        return self._cache
