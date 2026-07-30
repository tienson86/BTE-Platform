"""Simple mtime-aware cache for Knowledge infrastructure."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class _CacheEntry(Generic[T]):
    mtime: float
    value: T


class MtimeCache(Generic[T]):
    """Cache values keyed by path, invalidated when mtime changes."""

    def __init__(self) -> None:
        """Initialize an empty cache."""
        self._entries: dict[str, _CacheEntry[T]] = {}

    def clear(self) -> None:
        """Drop all cached entries."""
        self._entries.clear()

    def get(self, path: Path) -> T | None:
        """Return cached value when path mtime is unchanged."""
        key = str(path.resolve())
        entry = self._entries.get(key)
        if entry is None:
            return None
        try:
            mtime = path.stat().st_mtime
        except OSError:
            self._entries.pop(key, None)
            return None
        if entry.mtime != mtime:
            self._entries.pop(key, None)
            return None
        return entry.value

    def set(self, path: Path, value: T) -> T:
        """Store value with current path mtime."""
        key = str(path.resolve())
        mtime = path.stat().st_mtime
        self._entries[key] = _CacheEntry(mtime=mtime, value=value)
        return value

    def __len__(self) -> int:
        """Return number of cached entries."""
        return len(self._entries)
