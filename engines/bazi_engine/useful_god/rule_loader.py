"""
===============================================================================
Bazi Engine - Useful God Rule Loader
-------------------------------------------------------------------------------
File:
    bazi_engine/useful_god/rule_loader.py

Description:
    Rule Loader cho Dụng Thần Engine.

Version:
    1.1.0
===============================================================================
"""

from __future__ import annotations

from typing import Dict
from typing import List
from typing import Optional

from database.loader import DatabaseLoader


# =============================================================================
# DATABASE PATH
# =============================================================================

DATABASE_ROOT = "13_useful_god/"


STRENGTH_RULES_DATABASE = (
    DATABASE_ROOT +
    "01_strength_rules.csv"
)

SEASON_RULES_DATABASE = (
    DATABASE_ROOT +
    "02_season_rules.csv"
)

TEMPERATURE_RULES_DATABASE = (
    DATABASE_ROOT +
    "03_temperature_rules.csv"
)

PATTERN_RULES_DATABASE = (
    DATABASE_ROOT +
    "04_pattern_rules.csv"
)

SPECIAL_CASE_RULES_DATABASE = (
    DATABASE_ROOT +
    "05_special_case_rules.csv"
)

FOLLOW_PATTERN_RULES_DATABASE = (
    DATABASE_ROOT +
    "06_follow_pattern_rules.csv"
)

COMBINATION_RULES_DATABASE = (
    DATABASE_ROOT +
    "07_combination_rules.csv"
)

PRIORITY_RULES_DATABASE = (
    DATABASE_ROOT +
    "08_priority_rules.csv"
)


# =============================================================================
# EXCEPTIONS
# =============================================================================

class UsefulGodRuleLoaderError(
    Exception,
):
    """
    Base Exception.
    """


class UsefulGodRuleNotFoundError(
    UsefulGodRuleLoaderError,
):
    """
    Không tìm thấy Rule.
    """


# =============================================================================
# RULE LOADER
# =============================================================================

class UsefulGodRuleLoader:
    """
    Rule Loader cho Dụng Thần.
    """

    def __init__(
        self,
    ):

        self._loader = DatabaseLoader()

        self._strength_rules: List[dict] = []

        self._season_rules: List[dict] = []

        self._temperature_rules: List[dict] = []

        self._pattern_rules: List[dict] = []

        self._special_rules: List[dict] = []

        self._follow_pattern_rules: List[dict] = []

        self._combination_rules: List[dict] = []

        self._priority_rules: List[dict] = []

        self.reload()


    # -----------------------------------------------------------------
    # LOAD
    # -----------------------------------------------------------------

    def reload(
        self,
    ) -> None:
        """
        Load toàn bộ Rule Database.
        """

        self._strength_rules = self._loader.load_csv(
            STRENGTH_RULES_DATABASE
        )

        self._season_rules = self._loader.load_csv(
            SEASON_RULES_DATABASE
        )

        self._temperature_rules = self._loader.load_csv(
            TEMPERATURE_RULES_DATABASE
        )

        self._pattern_rules = self._loader.load_csv(
            PATTERN_RULES_DATABASE
        )

        self._special_rules = self._loader.load_csv(
            SPECIAL_CASE_RULES_DATABASE
        )

        self._follow_pattern_rules = self._loader.load_csv(
            FOLLOW_PATTERN_RULES_DATABASE
        )

        self._combination_rules = self._loader.load_csv(
            COMBINATION_RULES_DATABASE
        )

        self._priority_rules = self._loader.load_csv(
            PRIORITY_RULES_DATABASE
        )
          # -----------------------------------------------------------------
    # GET RULES
    # -----------------------------------------------------------------

    def get_strength_rules(
        self,
    ) -> List[dict]:
        """
        Quy tắc theo Thân Vượng/Nhược.
        """

        return self._strength_rules


    # -----------------------------------------------------------------

    def get_season_rules(
        self,
    ) -> List[dict]:
        """
        Quy tắc Điều Hậu theo mùa.
        """

        return self._season_rules


    # -----------------------------------------------------------------

    def get_temperature_rules(
        self,
    ) -> List[dict]:
        """
        Quy tắc Hàn - Nhiệt - Táo - Thấp.
        """

        return self._temperature_rules


    # -----------------------------------------------------------------

    def get_pattern_rules(
        self,
    ) -> List[dict]:
        """
        Quy tắc Chính Cách.
        """

        return self._pattern_rules


    # -----------------------------------------------------------------

    def get_special_rules(
        self,
    ) -> List[dict]:
        """
        Quy tắc Ngoại Lệ.
        """

        return self._special_rules


    # -----------------------------------------------------------------

    def get_follow_pattern_rules(
        self,
    ) -> List[dict]:
        """
        Quy tắc Tòng Cách.
        """

        return self._follow_pattern_rules


    # -----------------------------------------------------------------

    def get_combination_rules(
        self,
    ) -> List[dict]:
        """
        Quy tắc Hợp Hóa.
        """

        return self._combination_rules


    # -----------------------------------------------------------------

    def get_priority_rules(
        self,
    ) -> List[dict]:
        """
        Quy tắc Ưu Tiên.
        """

        return self._priority_rules


    # -----------------------------------------------------------------
    # QUERY
    # -----------------------------------------------------------------

    def find_priority(
        self,
        name: str,
    ) -> Optional[dict]:
        """
        Tìm Rule ưu tiên.
        """

        for rule in self._priority_rules:

            if rule.get("name") == name:

                return rule

        return None


    # -----------------------------------------------------------------
    # INFORMATION
    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, int]:
        """
        Thống kê Rule Database.
        """

        return {

            "strength_rules":

                len(self._strength_rules),

            "season_rules":

                len(self._season_rules),

            "temperature_rules":

                len(self._temperature_rules),

            "pattern_rules":

                len(self._pattern_rules),

            "special_rules":

                len(self._special_rules),

            "follow_pattern_rules":

                len(self._follow_pattern_rules),

            "combination_rules":

                len(self._combination_rules),

            "priority_rules":

                len(self._priority_rules),

        }


    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra trạng thái Rule Loader.
        """

        return (

            len(self._strength_rules) > 0

            and

            len(self._priority_rules) > 0

        )


    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload toàn bộ dữ liệu.
        """

        self.reload()


    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa cache trong RAM.
        """

        self._strength_rules.clear()

        self._season_rules.clear()

        self._temperature_rules.clear()

        self._pattern_rules.clear()

        self._special_rules.clear()

        self._follow_pattern_rules.clear()

        self._combination_rules.clear()

        self._priority_rules.clear()


    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> Dict[str, object]:
        """
        Thông tin Debug.
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
        """
        Tổng số Rule.
        """

        return (

            len(self._strength_rules)

            +

            len(self._season_rules)

            +

            len(self._temperature_rules)

            +

            len(self._pattern_rules)

            +

            len(self._special_rules)

            +

            len(self._follow_pattern_rules)

            +

            len(self._combination_rules)

            +

            len(self._priority_rules)

        )


    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<UsefulGodRuleLoader "

            f"rules={len(self)}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

useful_god_rule_loader = UsefulGodRuleLoader()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "UsefulGodRuleLoader",

    "UsefulGodRuleLoaderError",

    "UsefulGodRuleNotFoundError",

    "useful_god_rule_loader",

]
