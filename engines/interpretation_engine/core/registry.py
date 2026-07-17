"""
BTE Platform
Interpretation Engine

Registry

Quản lý đăng ký các Module của Engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(slots=True)
class ModuleInfo:
    """
    Thông tin một module.
    """

    name: str

    version: str

    description: str

    enabled: bool = True

    handler: Callable | None = None


class RegistryError(Exception):
    """Lỗi Registry."""


class Registry:

    def __init__(self):

        self._modules: dict[str, ModuleInfo] = {}

    def register(self, module: ModuleInfo):

        if module.name in self._modules:

            raise RegistryError(
                f"Module [{module.name}] đã tồn tại."
            )

        self._modules[module.name] = module

    def unregister(self, name: str):

        self._modules.pop(name, None)

    def exists(self, name: str):

        return name in self._modules

    def get(self, name: str):

        return self._modules[name]

    def list_modules(self):

        return sorted(self._modules.keys())

    def enabled_modules(self):

        return [

            module

            for module in self._modules.values()

            if module.enabled

        ]

    def clear(self):

        self._modules.clear()

    def count(self):

        return len(self._modules)
