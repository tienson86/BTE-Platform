"""
context.py
==========

Interpretation Context

Lưu toàn bộ dữ liệu đã tính toán để Rule Engine,
Sentence Generator và Report Builder sử dụng.

Đây là Data Hub của Interpretation Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class InterpretationContext:
    """
    Context dùng trong toàn bộ Interpretation Engine.

    Dữ liệu được lưu dưới dạng key-value.

    Ví dụ:

        bazi.day_master

        bazi.month_branch

        strength.level

        useful_god.primary

        shensha.names

        pattern.name

        luck.current
    """

    # ======================================================
    # Main Data
    # ======================================================

    data: dict[str, Any] = field(default_factory=dict)

    # ======================================================
    # Metadata
    # ======================================================

    metadata: dict[str, Any] = field(default_factory=dict)

    # ======================================================
    # Runtime Cache
    # ======================================================

    cache: dict[str, Any] = field(default_factory=dict)

    # ======================================================
    # Basic API
    # ======================================================

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.data[key] = value

        self.cache.pop(key, None)

    # ------------------------------------------------------

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        value = self.resolve(key)

        if value is None:
            return default

        return value

    # ------------------------------------------------------

    def exists(
        self,
        key: str,
    ) -> bool:

        return self.resolve(key) is not None

    # ======================================================
    # Resolve
    # ======================================================

    def resolve(
        self,
        path: str,
    ) -> Any:
        """
        Resolve theo đường dẫn.

        Ví dụ:

            bazi.day_master

            useful_god.primary

            pattern.name
        """

        if path in self.cache:
            return self.cache[path]

        parts = path.split(".")

        current: Any = self.data

        for part in parts:

            if current is None:
                return None

            if isinstance(current, dict):

                current = current.get(part)

            else:

                current = getattr(
                    current,
                    part,
                    None,
                )

        self.cache[path] = current

        return current

    # ======================================================
    # Metadata
    # ======================================================

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.metadata.get(
            key,
            default,
        )

    # ======================================================
    # Update
    # ======================================================

    def update(
        self,
        values: dict[str, Any],
    ) -> None:

        self.data.update(values)

        self.cache.clear()

    # ======================================================
    # Remove
    # ======================================================

    def remove(
        self,
        key: str,
    ) -> None:

        self.data.pop(
            key,
            None,
        )

        self.cache.clear()

    # ======================================================
    # Clear
    # ======================================================

    def clear(self) -> None:

        self.data.clear()

        self.cache.clear()

        self.metadata.clear()

    # ======================================================
    # Export
    # ======================================================

    def to_dict(self) -> dict[str, Any]:

        return dict(self.data)

    # ======================================================
    # Magic Methods
    # ======================================================

    def __getitem__(
        self,
        key: str,
    ) -> Any:

        return self.resolve(key)

    def __setitem__(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.set(key, value)

    def __contains__(
        self,
        key: str,
    ) -> bool:

        return self.exists(key)

    def __len__(self) -> int:

        return len(self.data)

    def __repr__(self) -> str:

        return (
            f"InterpretationContext("
            f"keys={len(self.data)}, "
            f"metadata={len(self.metadata)})"
        )
