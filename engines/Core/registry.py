"""
===============================================================================
BTE Platform - Core Registry
===============================================================================

Registry quản lý toàn bộ thành phần của Framework.

Author : BTE Platform
Version: 1.0.0
===============================================================================
"""

from .exceptions import (
    DuplicateRegistrationError,
    ComponentNotFoundError,
)


class Registry:
    """
    Registry dùng chung.
    """

    def __init__(self):

        self._items = {}

    def register(self, name, obj):

        if name in self._items:

            raise DuplicateRegistrationError(
                f"{name} already registered."
            )

        self._items[name] = obj

    def unregister(self, name):

        if name in self._items:

            del self._items[name]

    def get(self, name):

        if name not in self._items:

            raise ComponentNotFoundError(
                f"{name} not found."
            )

        return self._items[name]

    def exists(self, name):

        return name in self._items

    def names(self):

        return list(self._items.keys())

    def objects(self):

        return list(self._items.values())

    def clear(self):

        self._items.clear()

    def __len__(self):

        return len(self._items)

    def __contains__(self, item):

        return item in self._items


# =============================================================================
# Global Registries
# =============================================================================

EngineRegistry = Registry()

RuleRegistry = Registry()

TemplateRegistry = Registry()

ExporterRegistry = Registry()

ParserRegistry = Registry()

PluginRegistry = Registry()
