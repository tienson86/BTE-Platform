"""
cache.py
=========

Bộ nhớ đệm cho Interpretation Engine.

Mục tiêu:
- Không tính toán lại cùng một lá số.
- Tăng tốc diễn giải.
- Có thể thay bằng Redis hoặc Memcached trong tương lai.
"""

from typing import Any, Dict


class InterpretationCache:

    def __init__(self):
        self._cache: Dict[str, Any] = {}

    def has(self, key: str) -> bool:
        return key in self._cache

    def get(self, key: str):
        return self._cache.get(key)

    def set(self, key: str, value: Any):
        self._cache[key] = value

    def remove(self, key: str):
        self._cache.pop(key, None)

    def clear(self):
        self._cache.clear()

    def size(self) -> int:
        return len(self._cache)
