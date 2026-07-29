"""Load Feng Shui Engine static data files."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent


@lru_cache(maxsize=4)
def load_json(name: str) -> dict[str, Any]:
    """Load a JSON file from the engine data directory."""
    path = DATA_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))
