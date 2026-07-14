"""
===============================================================================
Bazi Engine - Base Rule Loader
-------------------------------------------------------------------------------
File:
    bazi_engine/core/base_rule_loader.py

Description:
    Lớp cơ sở cho tất cả Rule Loader.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from typing import Dict
from typing import List
from typing import Optional

from database.loader import DatabaseLoader


# =============================================================================
# BASE RULE LOADER
# =============================================================================

class BaseRuleLoader(ABC):
    """
    Lớp cơ sở của mọi Rule Loader.
    """

    def __init__(self):

        self._loader = DatabaseLoader()

        self._loaded = False

        self.reload()

    # -----------------------------------------------------------------
    # ABSTRACT
    # -----------------------------------------------------------------

    @abstractmethod
    def reload(
        self,
    ) -> None:
        """
        Nạp toàn bộ Rule Database.
        """

        raise NotImplementedError

    # -----------------------------------------------------------------

    @abstractmethod
    def statistics(
        self,
    ) -> Dict:
        """
        Thống kê Rule.
        """

        raise NotImplementedError

    # -----------------------------------------------------------------

    @abstractmethod
    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra trạng thái.
        """

        raise NotImplementedError

    # -----------------------------------------------------------------
    # COMMON CSV
    # -----------------------------------------------------------------

    def load_csv(
        self,
        path: str,
    ) -> List[dict]:
        """
        Đọc một file CSV.
        """

        return self._loader.load_csv(
            path
        )

    # -----------------------------------------------------------------

    def load_json(
        self,
        path: str,
    ):
        """
        Đọc JSON.
        """

        return self._loader.load_json(
            path
        )

    # -----------------------------------------------------------------

    def mark_loaded(
        self,
    ) -> None:

        self._loaded = True

    # -----------------------------------------------------------------

    @property
    def loaded(
        self,
    ) -> bool:

        return self._loaded
          # -----------------------------------------------------------------
    # COMMON QUERY
    # -----------------------------------------------------------------

    def find_by_code(
        self,
        rules: List[dict],
        code: str,
    ) -> Optional[dict]:
        """
        Tìm Rule theo mã.
        """

        for rule in rules:

            if rule.get("code") == code:

                return rule

        return None


    # -----------------------------------------------------------------

    def find_by_name(
        self,
        rules: List[dict],
        name: str,
    ) -> Optional[dict]:
        """
        Tìm Rule theo tên.
        """

        for rule in rules:

            if rule.get("name") == name:

                return rule

        return None


    # -----------------------------------------------------------------

    def filter_rules(
        self,
        rules: List[dict],
        **conditions,
    ) -> List[dict]:
        """
        Lọc Rule theo nhiều điều kiện.

        Ví dụ:
            filter_rules(
                rules,
                category="main",
                enabled="true",
            )
        """

        results: List[dict] = []

        for rule in rules:

            matched = True

            for key, value in conditions.items():

                if str(rule.get(key)) != str(value):

                    matched = False

                    break

            if matched:

                results.append(rule)

        return results


    # -----------------------------------------------------------------

    def sort_rules(
        self,
        rules: List[dict],
        key: str = "priority",
        reverse: bool = False,
    ) -> List[dict]:
        """
        Sắp xếp Rule.
        """

        return sorted(

            rules,

            key=lambda item: item.get(
                key,
                0,
            ),

            reverse=reverse,

        )


    # -----------------------------------------------------------------

    def count_rules(
        self,
        rules: List[dict],
    ) -> int:
        """
        Đếm số Rule.
        """

        return len(rules)


    # -----------------------------------------------------------------
    # COMMON OPERATIONS
    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload Rule Database.
        """

        self.reload()

        self.mark_loaded()


    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa trạng thái đã nạp.

        Lưu ý:
            Các RuleLoader kế thừa có thể override
            để xóa thêm các danh sách nội bộ.
        """

        self._loaded = False


    # -----------------------------------------------------------------

    def is_loaded(
        self,
    ) -> bool:
        """
        Kiểm tra trạng thái đã nạp.
        """

        return self.loaded


    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> Dict[str, object]:
        """
        Thông tin Debug.
        """

        return {

            "loader":
                self.__class__.__name__,

            "loaded":
                self.loaded,

            "health":
                self.health_check(),

            "statistics":
                self.statistics(),

        }
          # -----------------------------------------------------------------
    # MAGIC METHODS
    # -----------------------------------------------------------------

    def __len__(
        self,
    ) -> int:
        """
        Tổng số Rule.

        Mặc định lấy từ statistics().
        Các lớp con có thể override nếu cần.
        """

        stats = self.statistics()

        total = 0

        for value in stats.values():

            if isinstance(value, int):

                total += value

        return total


    # -----------------------------------------------------------------

    def __bool__(
        self,
    ) -> bool:
        """
        True nếu Rule Loader khả dụng.
        """

        return self.health_check()


    # -----------------------------------------------------------------

    def __contains__(
        self,
        code: str,
    ) -> bool:
        """
        Kiểm tra nhanh sự tồn tại của Rule theo mã.

        Lớp con nên override nếu hỗ trợ.
        """

        return False


    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"<{self.__class__.__name__} "

            f"loaded={self.loaded} "

            f"rules={len(self)}>"

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

        if not self.loaded:

            self.refresh()

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

    "BaseRuleLoader",

]
