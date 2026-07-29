"""
BTE Platform - Engine Factory.

Factory tạo hoặc lấy Engine từ Registry.
"""

from __future__ import annotations

from typing import Any

from .registry import registry


class EngineFactory:
    """
    Factory khởi tạo Engine.
    """

    @staticmethod
    def create(name: str) -> Any:
        """
        Luôn tạo mới một Engine.
        """
        return registry.create(name)

    @staticmethod
    def get(name: str) -> Any:
        """
        Lấy Engine từ Registry.
        Nếu Engine là singleton sẽ trả về cùng một instance.
        """
        return registry.get(name)

    @staticmethod
    def exists(name: str) -> bool:
        """
        Kiểm tra Engine đã được đăng ký.
        """
        return registry.exists(name)

    @staticmethod
    def registered() -> list[str]:
        """
        Danh sách Engine đã đăng ký.
        """
        return registry.list()

    @staticmethod
    def count() -> int:
        """
        Số lượng Engine.
        """
        return registry.count()

    @staticmethod
    def metadata(name: str):
        """
        Metadata của Engine.
        """
        return registry.metadata(name)

    @staticmethod
    def reset():
        """
        Xóa toàn bộ Singleton Instance.
        """
        registry.reset()

    @staticmethod
    def clear():
        """
        Xóa Registry.
        """
        registry.clear()


# Singleton dùng chung
engine_factory = EngineFactory()
