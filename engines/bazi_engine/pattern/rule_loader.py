"""
===============================================================================
Bazi Engine - Pattern Rule Loader
-------------------------------------------------------------------------------
File:
    bazi_engine/pattern/rule_loader.py

Description:
    Rule Loader cho Pattern Engine.

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
# DATABASE
# =============================================================================

DATABASE_ROOT = "14_pattern/"


MAIN_PATTERN_DATABASE = (
    DATABASE_ROOT +
    "01_main_pattern.csv"
)

FOLLOW_PATTERN_DATABASE = (
    DATABASE_ROOT +
    "02_follow_pattern.csv"
)

TRANSFORMATION_DATABASE = (
    DATABASE_ROOT +
    "03_transformation.csv"
)

SPECIAL_PATTERN_DATABASE = (
    DATABASE_ROOT +
    "04_special_pattern.csv"
)

PRIORITY_DATABASE = (
    DATABASE_ROOT +
    "05_pattern_priority.csv"
)

CONDITION_DATABASE = (
    DATABASE_ROOT +
    "06_pattern_conditions.csv"
)

SCORING_DATABASE = (
    DATABASE_ROOT +
    "07_pattern_scoring.csv"
)


# =============================================================================
# EXCEPTIONS
# =============================================================================

class PatternRuleLoaderError(
    Exception,
):
    """
    Base Exception.
    """


class PatternRuleNotFoundError(
    PatternRuleLoaderError,
):
    """
    Không tìm thấy Rule.
    """


# =============================================================================
# RULE LOADER
# =============================================================================

class PatternRuleLoader:
    """
    Rule Loader của Pattern Engine.
    """

    def __init__(
        self,
    ):

        self._loader = DatabaseLoader()

        self._main_patterns: List[dict] = []

        self._follow_patterns: List[dict] = []

        self._transformations: List[dict] = []

        self._special_patterns: List[dict] = []

        self._priority_rules: List[dict] = []

        self._condition_rules: List[dict] = []

        self._scoring_rules: List[dict] = []

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

        self._main_patterns = self._loader.load_csv(
            MAIN_PATTERN_DATABASE
        )

        self._follow_patterns = self._loader.load_csv(
            FOLLOW_PATTERN_DATABASE
        )

        self._transformations = self._loader.load_csv(
            TRANSFORMATION_DATABASE
        )

        self._special_patterns = self._loader.load_csv(
            SPECIAL_PATTERN_DATABASE
        )

        self._priority_rules = self._loader.load_csv(
            PRIORITY_DATABASE
        )

        self._condition_rules = self._loader.load_csv(
            CONDITION_DATABASE
        )

        self._scoring_rules = self._loader.load_csv(
            SCORING_DATABASE
        )
          # -----------------------------------------------------------------
    # GET RULES
    # -----------------------------------------------------------------

    def get_main_patterns(
        self,
    ) -> List[dict]:
        """
        Danh sách Chính Cách.
        """

        return self._main_patterns


    # -----------------------------------------------------------------

    def get_follow_patterns(
        self,
    ) -> List[dict]:
        """
        Danh sách Tòng Cách.
        """

        return self._follow_patterns


    # -----------------------------------------------------------------

    def get_transformations(
        self,
    ) -> List[dict]:
        """
        Danh sách Hóa Khí Cách.
        """

        return self._transformations


    # -----------------------------------------------------------------

    def get_special_patterns(
        self,
    ) -> List[dict]:
        """
        Danh sách Ngoại Cách.
        """

        return self._special_patterns


    # -----------------------------------------------------------------

    def get_priority_rules(
        self,
    ) -> List[dict]:
        """
        Quy tắc ưu tiên.
        """

        return self._priority_rules


    # -----------------------------------------------------------------

    def get_condition_rules(
        self,
    ) -> List[dict]:
        """
        Điều kiện thành/phá cách.
        """

        return self._condition_rules


    # -----------------------------------------------------------------

    def get_scoring_rules(
        self,
    ) -> List[dict]:
        """
        Quy tắc chấm điểm.
        """

        return self._scoring_rules


    # -----------------------------------------------------------------
    # QUERY
    # -----------------------------------------------------------------

    def find_pattern(
        self,
        code: str,
    ) -> Optional[dict]:
        """
        Tìm Cách Cục theo mã.
        """

        for pattern in self._main_patterns:

            if pattern.get("code") == code:

                return pattern

        for pattern in self._follow_patterns:

            if pattern.get("code") == code:

                return pattern

        for pattern in self._transformations:

            if pattern.get("code") == code:

                return pattern

        for pattern in self._special_patterns:

            if pattern.get("code") == code:

                return pattern

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

            "main_patterns":
                len(self._main_patterns),

            "follow_patterns":
                len(self._follow_patterns),

            "transformations":
                len(self._transformations),

            "special_patterns":
                len(self._special_patterns),

            "priority_rules":
                len(self._priority_rules),

            "condition_rules":
                len(self._condition_rules),

            "scoring_rules":
                len(self._scoring_rules),

        }


    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra trạng thái Rule Loader.
        """

        return (

            len(self._main_patterns) > 0

            and

            len(self._priority_rules) > 0

        )


    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload toàn bộ Rule Database.
        """

        self.reload()


    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa cache trong RAM.
        """

        self._main_patterns.clear()

        self._follow_patterns.clear()

        self._transformations.clear()

        self._special_patterns.clear()

        self._priority_rules.clear()

        self._condition_rules.clear()

        self._scoring_rules.clear()


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

            len(self._main_patterns)

            + len(self._follow_patterns)

            + len(self._transformations)

            + len(self._special_patterns)

            + len(self._priority_rules)

            + len(self._condition_rules)

            + len(self._scoring_rules)

        )


    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<PatternRuleLoader "

            f"rules={len(self)}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

pattern_rule_loader = PatternRuleLoader()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "PatternRuleLoader",

    "PatternRuleLoaderError",

    "PatternRuleNotFoundError",

    "pattern_rule_loader",

]
