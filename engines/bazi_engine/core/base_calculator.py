"""
===============================================================================
Bazi Engine - Base Calculator
-------------------------------------------------------------------------------
File:
    bazi_engine/core/base_calculator.py

Description:
    Lớp cơ sở cho toàn bộ các Calculator trong Bazi Engine.

Các chức năng chung:

    • Load dữ liệu CSV
    • Cache dữ liệu
    • Reload dữ liệu
    • Health Check
    • Statistics
    • Validation
    • Debug Utilities

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from typing import Any
from typing import Dict

from database.loader import DatabaseLoader
from database.cache import DatabaseCache


# =============================================================================
# EXCEPTION
# =============================================================================

class BaseCalculatorError(Exception):
    """Base Exception."""


# =============================================================================
# BASE CALCULATOR
# =============================================================================

class BaseCalculator(ABC):
    """
    Base class của toàn bộ Calculator.
    """

    # ---------------------------------------------------------------------

    def __init__(self):

        self._loader = DatabaseLoader()

        self._cache = DatabaseCache()

        self._loaded = False

    # ---------------------------------------------------------------------

    @property
    def loaded(self) -> bool:

        return self._loaded

    # ---------------------------------------------------------------------

    def mark_loaded(self):

        self._loaded = True

    # ---------------------------------------------------------------------

    def mark_unloaded(self):

        self._loaded = False

    # ---------------------------------------------------------------------

    def ensure_loaded(self):

        if not self._loaded:

            raise BaseCalculatorError(
                f"{self.__class__.__name__} chưa load dữ liệu."
            )

    # ---------------------------------------------------------------------

    @abstractmethod
    def reload(self):
        """
        Reload dữ liệu.
        """

    # ---------------------------------------------------------------------

    @abstractmethod
    def clear_cache(self):
        """
        Xóa cache.
        """

    # ---------------------------------------------------------------------

    @abstractmethod
    def statistics(self) -> Dict[str, int]:
        """
        Thống kê dữ liệu.
        """

    # ---------------------------------------------------------------------

    @abstractmethod
    def health_check(self) -> bool:
        """
        Kiểm tra dữ liệu.
        """

    # ---------------------------------------------------------------------

    def refresh(self):

        self.clear_cache()

        self.reload()

    # ---------------------------------------------------------------------

    def validate_not_none(
        self,
        value: Any,
        field_name: str,
    ):

        if value is None:

            raise ValueError(
                f"{field_name} không được None."
            )

    # ---------------------------------------------------------------------

    def validate_string(
        self,
        value: str,
        field_name: str,
    ):

        if not isinstance(value, str):

            raise TypeError(
                f"{field_name} phải là str."
            )

        if value.strip() == "":

            raise ValueError(
                f"{field_name} không được rỗng."
            )

    # ---------------------------------------------------------------------

    def validate_int(
        self,
        value: int,
        field_name: str,
    ):

        if not isinstance(value, int):

            raise TypeError(
                f"{field_name} phải là int."
            )

    # ---------------------------------------------------------------------

    def validate_dict(
        self,
        value: dict,
        field_name: str,
    ):

        if not isinstance(value, dict):

            raise TypeError(
                f"{field_name} phải là dict."
            )

    # ---------------------------------------------------------------------

    def debug(self) -> Dict[str, Any]:
        """
        Thông tin debug cơ bản.
        """

        return {

            "class": self.__class__.__name__,

            "loaded": self.loaded,

        }

    # ---------------------------------------------------------------------

    def __bool__(self):

        return self.loaded

    # ---------------------------------------------------------------------

    def __repr__(self):

        return (

            f"<{self.__class__.__name__} "

            f"loaded={self.loaded}>"

        )


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "BaseCalculator",

    "BaseCalculatorError",

]
