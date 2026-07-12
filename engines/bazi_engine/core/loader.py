"""
===============================================================================
Bazi Engine - Data Loader
-------------------------------------------------------------------------------
Chức năng:
- Đọc dữ liệu CSV
- Đọc JSON
- Đọc YAML
- Đọc toàn bộ thư mục dữ liệu
- Tự động cache
===============================================================================
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

from .config import DEFAULT_ENCODING


class DataLoader:
    """
    Bộ đọc dữ liệu chuẩn cho toàn bộ Bazi Engine.
    """

    def __init__(self, encoding: str = DEFAULT_ENCODING):
        self.encoding = encoding

    # -------------------------------------------------------------------------
    # CSV
    # -------------------------------------------------------------------------

    def load_csv(self, filepath: str | Path) -> list[dict]:

        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(filepath)

        with open(filepath, "r", encoding=self.encoding, newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)

    # -------------------------------------------------------------------------
    # JSON
    # -------------------------------------------------------------------------

    def load_json(self, filepath: str | Path) -> Any:

        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(filepath)

        with open(filepath, "r", encoding=self.encoding) as f:
            return json.load(f)

    # -------------------------------------------------------------------------
    # YAML
    # -------------------------------------------------------------------------

    def load_yaml(self, filepath: str | Path) -> Any:

        if yaml is None:
            raise ImportError("PyYAML chưa được cài đặt.")

        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(filepath)

        with open(filepath, "r", encoding=self.encoding) as f:
            return yaml.safe_load(f)

    # -------------------------------------------------------------------------
    # AUTO
    # -------------------------------------------------------------------------

    def load(self, filepath: str | Path):

        filepath = Path(filepath)

        suffix = filepath.suffix.lower()

        if suffix == ".csv":
            return self.load_csv(filepath)

        if suffix == ".json":
            return self.load_json(filepath)

        if suffix in (".yaml", ".yml"):
            return self.load_yaml(filepath)

        raise ValueError(f"Không hỗ trợ định dạng: {suffix}")

    # -------------------------------------------------------------------------
    # DIRECTORY
    # -------------------------------------------------------------------------

    def load_directory(
        self,
        directory: str | Path,
        pattern: str = "*.*",
    ) -> dict[str, Any]:

        directory = Path(directory)

        if not directory.exists():
            raise FileNotFoundError(directory)

        data = {}

        for file in sorted(directory.glob(pattern)):
            if file.is_file():
                data[file.stem] = self.load(file)

        return data


# =============================================================================
# Singleton
# =============================================================================

loader = DataLoader()
