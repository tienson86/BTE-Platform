"""
===============================================================================
Bazi Engine - Base Rule Calculator
-------------------------------------------------------------------------------
File:
    bazi_engine/core/base_rule_calculator.py

Description:
    Lớp cơ sở cho các Calculator sử dụng Rule Database.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from abc import abstractmethod

from typing import Any
from typing import Dict
from typing import List


from .base_calculator import (
    BaseCalculator,
)


# =============================================================================
# BASE RULE CALCULATOR
# =============================================================================

class BaseRuleCalculator(
    BaseCalculator,
):
    """
    Abstract Calculator sử dụng Rule Engine.
    """


    def __init__(
        self,
        rule_loader: Any,
    ):

        super().__init__()

        self._rule_loader = rule_loader


    # -----------------------------------------------------------------
    # PROPERTY
    # -----------------------------------------------------------------

    @property
    def rule_loader(
        self,
    ):
        """
        Truy cập Rule Loader.
        """

        return self._rule_loader


    # -----------------------------------------------------------------
    # ABSTRACT CONTEXT
    # -----------------------------------------------------------------

    @abstractmethod
    def build_context(
        self,
        *args,
        **kwargs,
    ) -> Dict:
        """
        Xây dựng Context tính toán.
        """

        raise NotImplementedError


    # -----------------------------------------------------------------
    # RULE COLLECTION
    # -----------------------------------------------------------------

    def collect_rules(
        self,
        context: Dict,
    ) -> List[dict]:
        """
        Thu thập Rule phù hợp.

        Mặc định:
            lấy toàn bộ Rule.

        Engine con có thể override.
        """

        return self.rule_loader.get_all_rules()


    # -----------------------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------------------

    def validate_rule(
        self,
        rule: dict,
        context: Dict,
    ) -> bool:
        """
        Kiểm tra Rule có hợp lệ không.

        Mặc định:
            luôn True.

        Engine con override.
        """

        return True
          # -----------------------------------------------------------------
    # FILTER RULES
    # -----------------------------------------------------------------

    def filter_valid_rules(
        self,
        rules: List[dict],
        context: Dict,
    ) -> List[dict]:
        """
        Lọc các Rule hợp lệ.

        Rule nào vượt qua validate_rule()
        sẽ được giữ lại.
        """

        valid = []

        for rule in rules:

            if self.validate_rule(
                rule,
                context,
            ):

                valid.append(rule)

        return valid


    # -----------------------------------------------------------------
    # BUILD CANDIDATES
    # -----------------------------------------------------------------

    def build_candidates(
        self,
        context: Dict,
    ) -> List[dict]:
        """
        Tạo danh sách Candidate Rule.

        Pipeline:

        Context
            |
            ▼
        collect_rules()
            |
            ▼
        filter_valid_rules()

        """

        rules = self.collect_rules(
            context
        )

        return self.filter_valid_rules(

            rules,

            context,

        )


    # -----------------------------------------------------------------
    # RULE SORT
    # -----------------------------------------------------------------

    def sort_rules(
        self,
        rules: List[dict],
    ) -> List[dict]:
        """
        Sắp xếp Rule theo độ ưu tiên.
        """

        return sorted(

            rules,

            key=lambda rule:

                (

                    int(

                        rule.get(
                            "priority",
                            0,
                        )

                    ),

                    float(

                        rule.get(
                            "score",
                            0,
                        )

                    ),

                ),

            reverse=True,

        )


    # -----------------------------------------------------------------
    # SCORE
    # -----------------------------------------------------------------

    def score_rule(
        self,
        rule: dict,
        context: Dict,
    ) -> float:
        """
        Tính điểm Rule.

        Engine con có thể override.
        """

        try:

            return float(

                rule.get(
                    "score",
                    0,
                )

            )

        except (

            ValueError,

            TypeError,

        ):

            return 0.0
              # -----------------------------------------------------------------
    # BUILD RESULT
    # -----------------------------------------------------------------

    def build_result(
        self,
        rules: List[dict],
        context: Dict,
    ):
        """
        Xây dựng Result.

        Calculator con bắt buộc override.
        """

        raise NotImplementedError


    # -----------------------------------------------------------------
    # CALCULATE FROM RULES
    # -----------------------------------------------------------------

    def calculate_from_rules(
        self,
        context: Dict,
    ):
        """
        Pipeline tính toán chung.

        Flow:

        Context

            ↓

        Candidate Rules

            ↓

        Sort Rules

            ↓

        Build Result

        """

        rules = self.build_candidates(
            context
        )


        rules = self.sort_rules(
            rules
        )


        return self.build_result(

            rules,

            context,

        )


    # -----------------------------------------------------------------
    # REFRESH
    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload Rule Database.
        """

        loader_refresh = getattr(

            self.rule_loader,

            "reload",

            None,

        )


        if callable(loader_refresh):

            loader_refresh()


        self.mark_loaded()


    # -----------------------------------------------------------------
    # CLEAR CACHE
    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa Rule Cache.
        """

        clear = getattr(

            self.rule_loader,

            "clear_cache",

            None,

        )


        if callable(clear):

            clear()


        self.mark_unloaded()


    # -----------------------------------------------------------------
    # STATISTICS
    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, Any]:
        """
        Thống kê Calculator.
        """

        loader_stats = {}


        statistics = getattr(

            self.rule_loader,

            "statistics",

            None,

        )


        if callable(statistics):

            loader_stats = statistics()


        return {

            "calculator":

                self.__class__.__name__,


            "loaded":

                self.loaded,


            "rules":

                loader_stats,

        }
          # -----------------------------------------------------------------
    # HEALTH CHECK
    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra trạng thái Calculator.
        """

        loader_health = getattr(

            self.rule_loader,

            "health_check",

            None,

        )

        if callable(loader_health):

            return (

                self.loaded

                and

                loader_health()

            )


        return self.loaded


    # -----------------------------------------------------------------
    # DEBUG
    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> Dict[str, Any]:
        """
        Thông tin Debug.
        """

        return {

            "calculator":

                self.__class__.__name__,


            "version":

                self.version,


            "loaded":

                self.loaded,


            "health":

                self.health_check(),


            "statistics":

                self.statistics(),

        }


    # -----------------------------------------------------------------
    # VERSION
    # -----------------------------------------------------------------

    @property
    def version(
        self,
    ) -> str:
        """
        Phiên bản Calculator.
        """

        return "1.0.0"


    # -----------------------------------------------------------------
    # MAGIC METHODS
    # -----------------------------------------------------------------

    def __contains__(
        self,
        code: str,
    ) -> bool:
        """
        Kiểm tra Rule tồn tại.

        Ví dụ:

            "SS001" in calculator

        """

        contains = getattr(

            self.rule_loader,

            "__contains__",

            None,

        )

        if callable(contains):

            return contains(code)


        return False


    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<BaseRuleCalculator "

            f"{self.__class__.__name__} "

            f"loaded={self.loaded}>"

        )


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "BaseRuleCalculator",

]
