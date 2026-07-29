"""
Plugin Manager

Quản lý Plugin và trường phái.
"""

from __future__ import annotations

import importlib
from pathlib import Path


class PluginError(Exception):
    pass


class PluginManager:

    def __init__(self):

        self.plugins = {}

    def load(self, module_path: str):

        try:

            module = importlib.import_module(module_path)

        except Exception as ex:

            raise PluginError(str(ex))

        name = getattr(module, "PLUGIN_NAME", module_path)

        self.plugins[name] = module

        return module

    def unload(self, name: str):

        self.plugins.pop(name, None)

    def get(self, name: str):

        return self.plugins[name]

    def exists(self, name: str):

        return name in self.plugins

    def list_plugins(self):

        return sorted(self.plugins.keys())

    def load_directory(self, package):

        package = importlib.import_module(package)

        package_path = Path(package.__file__).parent

        for file in package_path.glob("*.py"):

            if file.stem.startswith("_"):
                continue

            if file.stem == "__init__":
                continue

            self.load(f"{package.__name__}.{file.stem}")

    def clear(self):

        self.plugins.clear()
