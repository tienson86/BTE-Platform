"""
Base Result.

Kết quả chuẩn của mọi Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class BaseResult:

    success: bool = True

    message: str = ""

    error: str | None = None

    execution_time: float = 0.0

    data: dict[str, Any] = field(default_factory=dict)

    warnings: list[str] = field(default_factory=list)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "message": self.message,
            "error": self.error,
            "execution_time": self.execution_time,
            "data": self.data,
            "warnings": self.warnings,
        }
