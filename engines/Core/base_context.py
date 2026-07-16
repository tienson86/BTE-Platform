"""
Base Context.

Lớp cơ sở cho tất cả Context trong BTE Platform.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class BaseContext:
    """
    Context cơ sở truyền dữ liệu giữa các Engine.
    """

    request_id: str = ""

    source: str = ""

    version: str = "1.0"

    metadata: dict[str, Any] = field(default_factory=dict)

    extra: dict[str, Any] = field(default_factory=dict)

    def set(self, key: str, value: Any) -> None:
        self.extra[key] = value

    def get(self, key: str, default=None):
        return self.extra.get(key, default)

    def has(self, key: str) -> bool:
        return key in self.extra

    def update(self, values: dict[str, Any]) -> None:
        self.extra.update(values)

    def clear(self) -> None:
        self.extra.clear()

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "source": self.source,
            "version": self.version,
            "metadata": self.metadata,
            "extra": self.extra,
        }
