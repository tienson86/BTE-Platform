"""
===============================================================================
Bazi Engine - Strength Rule Loader
-------------------------------------------------------------------------------
File:
    bazi_engine/strength/rule_loader.py

Description:
    Nạp dữ liệu quy tắc Thân Vượng - Thân Nhược.

Version:
    1.0.0
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

STRENGTH_LEVEL_DATABASE = (
    "12_strength/"
    "strength_levels.csv"
)


STRENGTH_WEIGHT_DATABASE = (
    "12_strength/"
    "strength_weights.csv"
)


SUPPORT_RULE_DATABASE = (
    "12_strength/"
    "support_rules.csv"
)


DRAIN_RULE_DATABASE = (
    "12_strength/"
    "drain_rules.csv"
)


SEASON_DATABASE = (
    "12_strength/"
    "season_strength.csv"
)



# =============================================================================
# EXCEPTIONS
# =============================================================================

class StrengthRuleLoaderError(
    Exception,
):
    """
    Base Exception.
    """



class StrengthRuleNotFoundError(
    StrengthRuleLoaderError,
):
    """
    Không tìm thấy Rule.
    """



# =============================================================================
# RULE LOADER
# =============================================================================

class StrengthRuleLoader:
    """
    Loader dữ liệu Strength Engine.
    """

    def __init__(
        self,
    ):

        self._loader = DatabaseLoader()


        self._levels: List[dict] = []


        self._weights: Dict[str, dict] = {}


        self._support_rules: List[dict] = []


        self._drain_rules: List[dict] = []


        self._season_rules: List[dict] = []


        self.reload()



    # -----------------------------------------------------------------
    # LOAD
    # -----------------------------------------------------------------

    def reload(
        self,
    ) -> None:
        """
        Load toàn bộ dữ liệu.
        """

        self._load_levels()

        self._load_weights()

        self._load_support_rules()

        self._load_drain_rules()

        self._load_season_rules()



    # -----------------------------------------------------------------

    def _load_levels(
        self,
    ) -> None:
        """
        Load cấp độ Thân Vượng Nhược.
        """

        rows = self._loader.load_csv(
            STRENGTH_LEVEL_DATABASE
        )


        self._levels = rows



    # -----------------------------------------------------------------

    def _load_weights(
        self,
    ) -> None:
        """
        Load trọng số tính điểm.
        """

        rows = self._loader.load_csv(
            STRENGTH_WEIGHT_DATABASE
        )


        self._weights.clear()


        for row in rows:

            self._weights[
                row["factor"]
            ] = row



    # -----------------------------------------------------------------

    def _load_support_rules(
        self,
    ) -> None:
        """
        Load quy tắc trợ thân.
        """

        rows = self._loader.load_csv(
            SUPPORT_RULE_DATABASE
        )


        self._support_rules = rows
          # -----------------------------------------------------------------
    # LOAD DRAIN RULES
    # -----------------------------------------------------------------

    def _load_drain_rules(
        self,
    ) -> None:
        """
        Load quy tắc tiết khắc thân.
        """

        rows = self._loader.load_csv(
            DRAIN_RULE_DATABASE
        )


        self._drain_rules = rows



    # -----------------------------------------------------------------

    def _load_season_rules(
        self,
    ) -> None:
        """
        Load ảnh hưởng Tháng Lệnh.
        """

        rows = self._loader.load_csv(
            SEASON_DATABASE
        )


        self._season_rules = rows



    # -----------------------------------------------------------------
    # QUERY LEVEL
    # -----------------------------------------------------------------

    def get_level(
        self,
        score: float,
    ) -> Optional[dict]:
        """
        Lấy cấp độ Thân Vượng Nhược theo điểm.
        """

        for level in self._levels:

            minimum = float(
                level["min_score"]
            )

            maximum = float(
                level["max_score"]
            )


            if minimum <= score <= maximum:

                return level


        return None



    # -----------------------------------------------------------------
    # QUERY WEIGHT
    # -----------------------------------------------------------------

    def get_weight(
        self,
        factor: str,
    ) -> float:
        """
        Lấy trọng số yếu tố.
        """

        rule = self._weights.get(
            factor
        )


        if not rule:

            return 0.0


        return float(
            rule["weight"]
        )



    # -----------------------------------------------------------------
    # SUPPORT
    # -----------------------------------------------------------------

    def get_support_rules(
        self,
    ) -> List[dict]:
        """
        Lấy quy tắc trợ thân.
        """

        return self._support_rules



    # -----------------------------------------------------------------

    def get_support_rule(
        self,
        element: str,
    ) -> Optional[dict]:
        """
        Lấy quy tắc trợ thân theo Ngũ Hành.
        """

        for rule in self._support_rules:

            if rule.get(
                "element"
            ) == element:

                return rule


        return None



    # -----------------------------------------------------------------
    # DRAIN
    # -----------------------------------------------------------------

    def get_drain_rules(
        self,
    ) -> List[dict]:
        """
        Lấy quy tắc tiết khắc.
        """

        return self._drain_rules



    # -----------------------------------------------------------------

    def get_drain_rule(
        self,
        element: str,
    ) -> Optional[dict]:
        """
        Lấy quy tắc tiết khắc theo Ngũ Hành.
        """

        for rule in self._drain_rules:

            if rule.get(
                "element"
            ) == element:

                return rule


        return None



    # -----------------------------------------------------------------
    # SEASON
    # -----------------------------------------------------------------

    def get_season_rule(
        self,
        branch: str,
    ) -> Optional[dict]:
        """
        Lấy ảnh hưởng Tháng Lệnh.
        """

        for rule in self._season_rules:

            if rule.get(
                "branch"
            ) == branch:

                return rule


        return None



    # -----------------------------------------------------------------
    # INFORMATION
    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, int]:
        """
        Thống kê Rule.
        """

        return {

            "levels":

                len(self._levels),


            "weights":

                len(self._weights),


            "support_rules":

                len(self._support_rules),


            "drain_rules":

                len(self._drain_rules),


            "season_rules":

                len(self._season_rules),

        }



    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra dữ liệu.
        """

        return (

            len(self._levels) > 0

            and

            len(self._weights) > 0

            and

            len(self._season_rules) > 0

        )



    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload Database.
        """

        self.reload()



    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa dữ liệu RAM.
        """

        self._levels.clear()

        self._weights.clear()

        self._support_rules.clear()

        self._drain_rules.clear()

        self._season_rules.clear()



    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> Dict[str, object]:
        """
        Debug thông tin.
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

        return (

            len(self._levels)

            +

            len(self._weights)

        )



    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<StrengthRuleLoader "

            f"levels={len(self._levels)} "

            f"weights={len(self._weights)}>"

        )



# =============================================================================
# SINGLETON
# =============================================================================

strength_rule_loader = StrengthRuleLoader()



# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "StrengthRuleLoader",

    "StrengthRuleLoaderError",

    "StrengthRuleNotFoundError",

    "strength_rule_loader",

]
