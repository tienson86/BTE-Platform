"""
===============================================================================
Bazi Engine - Utilities
-------------------------------------------------------------------------------
Các hàm tiện ích dùng chung.

Lưu ý:
- Không chứa thuật toán Bát Tự.
- Không chứa nghiệp vụ.
===============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


# =============================================================================
# STRING
# =============================================================================

def normalize_text(text: str) -> str:
    """
    Chuẩn hóa chuỗi.
    """

    return text.strip()


# =============================================================================
# SAFE CONVERT
# =============================================================================

def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# =============================================================================
# PATH
# =============================================================================

def ensure_directory(path: str | Path) -> Path:
    """
    Tạo thư mục nếu chưa tồn tại.
    """

    path = Path(path)

    path.mkdir(parents=True, exist_ok=True)

    return path


# =============================================================================
# COLLECTION
# =============================================================================

def flatten(items: list[list]) -> list:
    """
    Làm phẳng danh sách.
    """

    return [item for sub in items for item in sub]


def unique(items: list) -> list:
    """
    Loại bỏ phần tử trùng.
    """

    return list(dict.fromkeys(items))


# =============================================================================
# DICTIONARY
# =============================================================================

def deep_merge(dict1: dict, dict2: dict) -> dict:
    """
    Gộp hai dictionary.
    """

    result = dict1.copy()

    for key, value in dict2.items():

        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value

    return result


# =============================================================================
# CHECK
# =============================================================================

def is_empty(value: Any) -> bool:
    return value is None or value == ""


def not_empty(value: Any) -> bool:
    return not is_empty(value)
