"""
Engine Registry.

Quản lý đăng ký và khởi tạo các Engine trong BTE Platform.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(frozen=True)
class RegistryItem:
    """
    Thông tin một Engine đã đăng ký.
    """

    name: str
    engine_class: type
    version: str = "1.0.0"
    description: str = ""
    singleton: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


class EngineRegistry:
    """
    Registry quản lý toàn bộ Engine.
    """

    def __init__(self):

        self._items: dict[str, RegistryItem] = {}

        self._instances: dict[str, Any] = {}

    # =========================================================
    # Register
    # =========================================================

    def register(
        self,
        name: str,
        engine_class: type,
        *,
        version: str = "1.0.0",
        description: str = "",
        singleton: bool = True,
        metadata: dict[str, Any] | None = None,
    ) -> None:

        if name in self._items:
            raise ValueError(
                f"Engine '{name}' đã được đăng ký."
            )

        self._items[name] = RegistryItem(
            name=name,
            engine_class=engine_class,
            version=version,
            description=description,
            singleton=singleton,
            metadata=metadata or {},
        )

    # =========================================================
    # Remove
    # =========================================================

    def unregister(self, name: str) -> None:

        self._items.pop(name, None)
        self._instances.pop(name, None)

    # =========================================================
    # Query
    # =========================================================

    def exists(self, name: str) -> bool:

        return name in self._items

    def list(self) -> list[str]:

        return sorted(self._items.keys())

    def count(self) -> int:

        return len(self._items)

    def metadata(self, name: str) -> RegistryItem:

        return self._items[name]

    # =========================================================
    # Create / Get
    # =========================================================

    def create(self, name: str):

        if name not in self._items:
            raise KeyError(
                f"Không tìm thấy Engine '{name}'."
            )

        item = self._items[name]

        return item.engine_class()

    def get(self, name: str):

        if name not in self._items:
            raise KeyError(
                f"Không tìm thấy Engine '{name}'."
            )

        item = self._items[name]

        if not item.singleton:
            return item.engine_class()

        if name not in self._instances:
            self._instances[name] = item.engine_class()

        return self._instances[name]

    # =========================================================
    # Maintenance
    # =========================================================

    def clear(self):

        self._items.clear()
        self._instances.clear()

    def reset(self):

        self._instances.clear()


# Singleton Registry dùng chung toàn hệ thống
registry = EngineRegistry()
