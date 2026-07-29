"""
Score Loader

Quản lý toàn bộ dữ liệu của Score Engine.

Chức năng
---------
- Load một file CSV
- Load một nhóm Rule
- Load toàn bộ Database
- Cache dữ liệu
- Reload dữ liệu
- Kiểm tra tồn tại
"""

from pathlib import Path
from typing import Dict, List

import pandas as pd


class ScoreLoader:

    def __init__(self, database_path):

        requested_path = Path(database_path)

        self.requested_path = requested_path
        self.database_path = self._resolve_database_path(
            requested_path
        )

        self.cache: Dict[str, pd.DataFrame] = {}

    def _resolve_database_path(self, requested_path: Path) -> Path:

        if requested_path.name == "13_score_engine":
            replacement = requested_path.parent / "15_score_engine"

            if replacement.exists():
                requested_path.mkdir(
                    parents=True,
                    exist_ok=True
                )

                return replacement

        if requested_path.exists():
            return requested_path

        return requested_path

    # =====================================================
    # Load một file
    # =====================================================

    def load_csv(self, relative_path: str) -> pd.DataFrame:

        relative_path = relative_path.replace("\\", "/")

        if relative_path in self.cache:
            return self.cache[relative_path]

        path = self.database_path / relative_path

        if not path.exists():
            raise FileNotFoundError(path)

        df = pd.read_csv(path)

        self.cache[relative_path] = df

        return df

    # =====================================================
    # Load toàn bộ file CSV trong một thư mục
    # =====================================================

    def load_group(self, group_name: str) -> Dict[str, pd.DataFrame]:

        folder = self.database_path / group_name

        if not folder.exists():
            raise FileNotFoundError(folder)

        result = {}

        csv_files = sorted(folder.glob("*.csv"))

        for csv_file in csv_files:

            relative = str(
                csv_file.relative_to(self.database_path)
            ).replace("\\", "/")

            result[csv_file.stem] = self.load_csv(relative)

        return result

    # =====================================================
    # Load toàn bộ Database
    # =====================================================

    def load_all(self):

        result = {}

        for csv_file in sorted(
            self.database_path.rglob("*.csv")
        ):

            relative = str(
                csv_file.relative_to(self.database_path)
            ).replace("\\", "/")

            result[relative] = self.load_csv(relative)

        return result

    # =====================================================
    # Cache
    # =====================================================

    def clear_cache(self):

        self.cache.clear()

    def reload(self):

        self.clear_cache()

        return self.load_all()

    # =====================================================
    # Utility
    # =====================================================

    def exists(self, relative_path: str) -> bool:

        path = self.database_path / relative_path

        return path.exists()

    def list_groups(self) -> List[str]:

        groups = []

        for item in sorted(self.database_path.iterdir()):

            if item.is_dir():
                groups.append(item.name)

        return groups

    def list_files(self, group_name: str) -> List[str]:

        folder = self.database_path / group_name

        if not folder.exists():
            return []

        return sorted([
            f.name
            for f in folder.glob("*.csv")
        ])

    def cache_size(self) -> int:

        return len(self.cache)

    def cache_keys(self):

        return list(self.cache.keys())

    def info(self):

        return {
            "database": str(self.database_path),
            "groups": self.list_groups(),
            "cached_files": self.cache_size(),
            "cache_keys": self.cache_keys(),
        }
