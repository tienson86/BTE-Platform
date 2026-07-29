"""
registry.py
===========

Operator Registry.

Tự động phát hiện và đăng ký Operator.

Chỉ cần tạo thêm file trong operators/
là Registry sẽ tự nạp.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import Dict, Iterable

from .operators.base import BaseOperator


class OperatorRegistry:

    def __init__(self):

        self._operators: Dict[str, BaseOperator] = {}

    # =====================================================
    # Register
    # =====================================================

    def register(
        self,
        operator: BaseOperator,
    ):

        name = operator.operator

        if name in self._operators:

            raise ValueError(
                f"Operator '{name}' đã tồn tại."
            )

        self._operators[name] = operator

    def unregister(self, name: str):

        self._operators.pop(name, None)

    # =====================================================
    # Auto Discovery
    # =====================================================

    def load_builtin(self):

        package = importlib.import_module(
            "engines.interpretation_engine.rule_engine.operators"
        )

        self.load_package(package)

    def load_package(
        self,
        package,
    ):

        for _, module_name, _ in pkgutil.iter_modules(
            package.__path__
        ):

            if module_name.startswith("_"):
                continue

            module = importlib.import_module(
                f"{package.__name__}.{module_name}"
            )

            self.load_module(module)

    def load_module(
        self,
        module,
    ):

        for _, cls in inspect.getmembers(
            module,
            inspect.isclass,
        ):

            if cls is BaseOperator:
                continue

            if not issubclass(cls, BaseOperator):
                continue

            operator = cls()

            self.register(operator)

    # =====================================================
    # Query
    # =====================================================

    def get(
        self,
        name: str,
    ) -> BaseOperator:

        if name not in self._operators:

            raise KeyError(
                f"Không tìm thấy Operator '{name}'."
            )

        return self._operators[name]

    def has(self, name: str) -> bool:

        return name in self._operators

    def all(self):

        return self._operators.values()

    def names(self):

        return sorted(
            self._operators.keys()
        )

    def clear(self):

        self._operators.clear()

    @property
    def count(self):

        return len(self._operators)

    def __len__(self):

        return len(self._operators)

    def __contains__(self, item):

        return item in self._operators

    def __repr__(self):

        return (
            f"OperatorRegistry("
            f"{self.count} operators)"
        )
