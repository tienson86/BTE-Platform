"""Read-only pack reader contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class PackReaderInterface(ABC):
    """Read-only access to pack resources. Must not mutate Pack 01."""

    @abstractmethod
    def read(self, pack_id: str, resource_key: str) -> Any:
        """Read a pack resource without mutation."""

    @abstractmethod
    def is_read_only(self, pack_id: str) -> bool:
        """Return whether the pack is read-only for Pack 03."""
