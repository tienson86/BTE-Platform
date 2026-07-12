"""
===============================================================================
Bazi Engine - Service Registry
-------------------------------------------------------------------------------
Đăng ký và quản lý các Service / Calculator dùng chung.

Nguyên tắc:
- Chỉ quản lý đối tượng.
- Không chứa nghiệp vụ.
- Không tạo vòng phụ thuộc giữa các module.
===============================================================================
"""

from __future__ import annotations

from typing import Any


class ServiceRegistry:
    """
    Registry dùng để đăng ký và truy xuất các Service.
    """

    def __init__(self) -> None:
        self._services: dict[str, Any] = {}

    # -------------------------------------------------------------------------
    # REGISTER
    # -------------------------------------------------------------------------

    def register(self, name: str, service: Any) -> None:

        if name in self._services:
            raise ValueError(
                f"Service '{name}' đã được đăng ký."
            )

        self._services[name] = service

    # -------------------------------------------------------------------------
    # GET
    # -------------------------------------------------------------------------

    def get(self, name: str) -> Any:

        if name not in self._services:
            raise KeyError(
                f"Service '{name}' chưa được đăng ký."
            )

        return self._services[name]

    # -------------------------------------------------------------------------
    # EXISTS
    # -------------------------------------------------------------------------

    def exists(self, name: str) -> bool:
        return name in self._services

    # -------------------------------------------------------------------------
    # REMOVE
    # -------------------------------------------------------------------------

    def remove(self, name: str) -> None:
        self._services.pop(name, None)

    # -------------------------------------------------------------------------
    # CLEAR
    # -------------------------------------------------------------------------

    def clear(self) -> None:
        self._services.clear()

    # -------------------------------------------------------------------------
    # LIST
    # -------------------------------------------------------------------------

    def names(self) -> list[str]:
        return sorted(self._services.keys())

    # -------------------------------------------------------------------------
    # COUNT
    # -------------------------------------------------------------------------

    def count(self) -> int:
        return len(self._services)

    # -------------------------------------------------------------------------
    # INFO
    # -------------------------------------------------------------------------

    def info(self) -> dict[str, Any]:

        return {
            "count": self.count(),
            "services": self.names(),
        }


# =============================================================================
# GLOBAL REGISTRY
# =============================================================================

registry = ServiceRegistry()
