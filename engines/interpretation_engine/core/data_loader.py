"""
Data Loader

Đọc CSV / JSON.
Không thực hiện validate.
"""

from __future__ import annotations

import csv
import json

from pathlib import Path


class DataLoader:

    @staticmethod
    def load_csv(path: str | Path):

        path = Path(path)

        with open(path, "r", encoding="utf-8-sig") as f:

            reader = csv.DictReader(f)

            return list(reader)

    @staticmethod
    def load_json(path: str | Path):

        path = Path(path)

        with open(path, "r", encoding="utf-8") as f:

            return json.load(f)
