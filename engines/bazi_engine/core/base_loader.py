"""
===============================================================================
Bazi Engine - Base Loader
-------------------------------------------------------------------------------
File:
    bazi_engine/core/base_loader.py

Description:
    Bộ nạp dữ liệu chuẩn cho Bazi Engine.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from database.loader import DatabaseLoader


class BaseLoader:
    """
    Base Loader cho toàn bộ Bazi Engine.
    """

    def __init__(self):

        self._loader = DatabaseLoader()

        self._cache: Dict[str, Any] = {}

    # ------------------------------------------------------------------

    @property
    def cache(self) -> Dict[str, Any]:
        return self._cache

    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Xóa cache."""

        self._cache.clear()

    # ------------------------------------------------------------------

    def has(self, key: str) -> bool:
        """Kiểm tra cache."""

        return key in self._cache

    # ------------------------------------------------------------------

    def get(self, key: str) -> Any:
        """Lấy dữ liệu cache."""

        return self._cache.get(key)

    # ------------------------------------------------------------------

    def put(
        self,
        key: str,
        value: Any,
    ) -> None:
        """Lưu cache."""

        self._cache[key] = value

    # ------------------------------------------------------------------

    def load_csv(
        self,
        path: str,
        cache_key: Optional[str] = None,
    ) -> List[Dict]:
        """
        Đọc file CSV.
        """

        key = cache_key or path

        if key in self._cache:

            return self._cache[key]

        rows = self._loader.load_csv(path)

        self._cache[key] = rows

        return rows

    # ------------------------------------------------------------------

    def load_dict(
        self,
        path: str,
        key_field: str,
        cache_key: Optional[str] = None,
    ) -> Dict[Any, Dict]:
        """
        Đọc CSV thành Dictionary.
        """

        rows = self.load_csv(path, cache_key)

        result = {}

        for row in rows:

            result[row[key_field]] = row

        return result

    # ------------------------------------------------------------------

    def load_index_dict(
        self,
        path: str,
        cache_key: Optional[str] = None,
    ) -> Dict[int, Dict]:
        """
        Đọc CSV theo index.
        """

        rows = self.load_csv(path, cache_key)

        result = {}

        for row in rows:

            result[int(row["index"])] = row

        return result

    # ------------------------------------------------------------------

    def statistics(self) -> Dict[str, int]:

        return {

            "cache_items": len(self._cache),

        }

    # ------------------------------------------------------------------

    def __len__(self):

        return len(self._cache)

    # ------------------------------------------------------------------

    def __repr__(self):

        return (

            f"<BaseLoader "

            f"cache={len(self._cache)}>"

        )


__all__ = [

    "BaseLoader",

]
