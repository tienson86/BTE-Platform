"""
===============================================================================
Bazi Engine - Base Service
-------------------------------------------------------------------------------
File:
    bazi_engine/core/base_service.py

Description:
    Lớp cơ sở cho toàn bộ Service của Bazi Engine.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from typing import Any
from typing import Dict


# =============================================================================
# BASE SERVICE
# =============================================================================

class BaseService(ABC):
    """
    Lớp cơ sở của mọi Service.
    """

    def __init__(
        self,
        calculator: Any,
    ):

        self._calculator = calculator


    # -----------------------------------------------------------------
    # ABSTRACT
    # -----------------------------------------------------------------

    @abstractmethod
    def calculate(
        self,
        *args,
        **kwargs,
    ):
        """
        API tính toán chính.
        """

        raise NotImplementedError


    # -----------------------------------------------------------------
    # COMMON PROPERTIES
    # -----------------------------------------------------------------

    @property
    def calculator(
        self,
    ) -> Any:
        """
        Truy cập Calculator.
        """

        return self._calculator


    # -----------------------------------------------------------------

    @property
    def version(
        self,
    ) -> str:
        """
        Phiên bản Service.

        Mặc định lấy từ Calculator.
        """

        return getattr(
            self._calculator,
            "version",
            "1.0.0",
        )


    # -----------------------------------------------------------------
    # COMMON STATUS
    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra trạng thái Service.
        """

        checker = getattr(
            self._calculator,
            "health_check",
            None,
        )

        if callable(checker):

            return checker()

        return True


    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload dữ liệu.
        """

        refresh = getattr(
            self._calculator,
            "refresh",
            None,
        )

        if callable(refresh):

            refresh()


    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa cache.
        """

        clear = getattr(
            self._calculator,
            "clear_cache",
            None,
        )

        if callable(clear):

            clear()
              # -----------------------------------------------------------------
    # COMMON INFORMATION
    # -----------------------------------------------------------------

    @property
    def service_name(
        self,
    ) -> str:
        """
        Tên Service.
        """

        return self.__class__.__name__


    # -----------------------------------------------------------------

    @property
    def calculator_name(
        self,
    ) -> str:
        """
        Tên Calculator.
        """

        return self._calculator.__class__.__name__


    # -----------------------------------------------------------------
    # COMMON STATISTICS
    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, object]:
        """
        Thống kê Service.
        """

        statistics = getattr(
            self._calculator,
            "statistics",
            None,
        )

        calculator_statistics = {}

        if callable(statistics):

            calculator_statistics = statistics()

        return {

            "service":
                self.service_name,

            "calculator":
                self.calculator_name,

            "version":
                self.version,

            "health":
                self.health_check(),

            "calculator_statistics":
                calculator_statistics,

        }


    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> Dict[str, object]:
        """
        Thông tin Debug.
        """

        return {

            "service":
                self.service_name,

            "calculator":
                self.calculator_name,

            "version":
                self.version,

            "health":
                self.health_check(),

            "statistics":
                self.statistics(),

            "calculator_repr":
                repr(self._calculator),

        }


    # -----------------------------------------------------------------
    # COMMON VERIFY
    # -----------------------------------------------------------------

    def available(
        self,
    ) -> bool:
        """
        Service sẵn sàng hoạt động.
        """

        return self.health_check()


    # -----------------------------------------------------------------

    def verify(
        self,
        *args,
        **kwargs,
    ) -> bool:
        """
        Kiểm tra khả năng tính toán.

        Mặc định:
            Gọi calculate().
        """

        try:

            self.calculate(
                *args,
                **kwargs,
            )

            return True

        except Exception:

            return False


    # -----------------------------------------------------------------

    def ping(
        self,
    ) -> Dict[str, str]:
        """
        Kiểm tra nhanh trạng thái Service.
        """

        return {

            "service":
                self.service_name,

            "status":
                "healthy"
                if self.health_check()
                else "unhealthy",

            "version":
                self.version,

        }
          # -----------------------------------------------------------------
    # MAGIC METHODS
    # -----------------------------------------------------------------

    def __bool__(
        self,
    ) -> bool:
        """
        True nếu Service hoạt động bình thường.
        """

        return self.health_check()


    # -----------------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        """
        Chuỗi mô tả ngắn.
        """

        return (

            f"{self.service_name}"

            f"(version={self.version})"

        )


    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        """
        Chuỗi Debug.
        """

        return (

            f"<{self.service_name} "

            f"calculator={self.calculator_name} "

            f"version={self.version} "

            f"health={self.health_check()}>"

        )


    # -----------------------------------------------------------------
    # CONTEXT MANAGER
    # -----------------------------------------------------------------

    def __enter__(
        self,
    ):
        """
        Hỗ trợ sử dụng với câu lệnh 'with'.
        """

        return self


    # -----------------------------------------------------------------

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> bool:
        """
        Kết thúc Context Manager.

        Không chặn Exception.
        """

        return False


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "BaseService",

]
