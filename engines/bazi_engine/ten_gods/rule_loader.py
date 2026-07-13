"""
===============================================================================
Bazi Engine - Ten Gods Rule Loader
-------------------------------------------------------------------------------
File:
    bazi_engine/ten_gods/rule_loader.py

Description:
    Nạp và quản lý Rule Database của Thập Thần.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

from database.loader import DatabaseLoader


# =============================================================================
# CONSTANTS
# =============================================================================

RULE_DATABASE = "10_ten_gods/ten_gods.csv"

DESCRIPTION_DATABASE = (
    "10_ten_gods/ten_gods_description.csv"
)


# =============================================================================
# EXCEPTIONS
# =============================================================================

class TenGodRuleLoaderError(Exception):
    """Base Exception."""


class TenGodRuleNotFoundError(
    TenGodRuleLoaderError,
):
    """Không tìm thấy Rule."""


# =============================================================================
# RULE LOADER
# =============================================================================

class TenGodRuleLoader:
    """
    Nạp Rule Database của Thập Thần.
    """

    def __init__(self):

        self._loader = DatabaseLoader()

        self._rules: Dict[
            tuple[str, str],
            dict,
        ] = {}

        self._descriptions: Dict[
            str,
            dict,
        ] = {}

        self.reload()

    # -----------------------------------------------------------------

    def reload(
        self,
    ) -> None:

        self._load_rules()

        self._load_descriptions()

    # -----------------------------------------------------------------

    def _load_rules(
        self,
    ) -> None:

        rows = self._loader.load_csv(
            RULE_DATABASE
        )

        self._rules.clear()

        for row in rows:

            key = (

                row["day_master"],

                row["target_stem"],

            )

            self._rules[key] = row

    # -----------------------------------------------------------------

    def _load_descriptions(
        self,
    ) -> None:

        rows = self._loader.load_csv(
            DESCRIPTION_DATABASE
        )

        self._descriptions.clear()

        for row in rows:

            self._descriptions[
                row["code"]
            ] = row
              # -----------------------------------------------------------------
    # RULE API
    # -----------------------------------------------------------------

    def has_rule(
        self,
        day_master: str,
        target_stem: str,
    ) -> bool:
        """
        Kiểm tra Rule có tồn tại hay không.
        """

        return (

            day_master,
            target_stem,

        ) in self._rules

    # -----------------------------------------------------------------

    def get_rule(
        self,
        day_master: str,
        target_stem: str,
    ) -> dict:
        """
        Lấy Rule Thập Thần.
        """

        key = (

            day_master,

            target_stem,

        )

        if key not in self._rules:

            raise TenGodRuleNotFoundError(

                f"Không tìm thấy Rule "

                f"({day_master} -> {target_stem})"

            )

        return self._rules[key]

    # -----------------------------------------------------------------

    def get_description(
        self,
        code: str,
    ) -> Optional[dict]:
        """
        Lấy dữ liệu mô tả Thập Thần.
        """

        return self._descriptions.get(
            code
        )

    # -----------------------------------------------------------------

    def get_all_rules(
        self,
    ) -> List[dict]:
        """
        Danh sách toàn bộ Rule.
        """

        return list(
            self._rules.values()
        )

    # -----------------------------------------------------------------

    def get_all_descriptions(
        self,
    ) -> List[dict]:
        """
        Danh sách mô tả.
        """

        return list(
            self._descriptions.values()
        )

    # -----------------------------------------------------------------

    def get_codes(
        self,
    ) -> List[str]:
        """
        Danh sách mã Thập Thần.
        """

        return sorted(
            self._descriptions.keys()
        )

    # -----------------------------------------------------------------
    # CACHE
    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa dữ liệu đã nạp.
        """

        self._rules.clear()

        self._descriptions.clear()

    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload Rule Database.
        """

        self.clear_cache()

        self.reload()

    # -----------------------------------------------------------------
    # INFORMATION
    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, int]:
        """
        Thống kê dữ liệu.
        """

        return {

            "rules":
                len(self._rules),

            "descriptions":
                len(self._descriptions),

            "codes":
                len(self.get_codes()),

        }

    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra tính đầy đủ của dữ liệu.
        """

        if len(self._rules) != 100:
            return False

        if len(self._descriptions) != 10:
            return False

        return True

    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> Dict[str, object]:
        """
        Thông tin debug.
        """

        return {

            "health":
                self.health_check(),

            "statistics":
                self.statistics(),

        }

    # -----------------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self._rules
        )

    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        stats = self.statistics()

        return (

            "<TenGodRuleLoader "

            f"rules={stats['rules']} "

            f"codes={stats['codes']}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

ten_god_rule_loader = TenGodRuleLoader()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "TenGodRuleLoader",

    "TenGodRuleLoaderError",

    "TenGodRuleNotFoundError",

    "ten_god_rule_loader",

]
